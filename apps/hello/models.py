from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import StringIO
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import datetime

class MyContacts(models.Model):
    name = models.CharField(max_length=70)
    surname = models.CharField(max_length=90)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=90)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField()
    exp = models.TextField(blank=True, null=True)
    skype = models.CharField(max_length=50)
    other_contacts = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='hello/photos/', blank=True, null=True)


    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        width = 200
        height = 200
        size = (width, height)
        if self.photo:
            image = Image.open(StringIO.StringIO(self.photo.read()))
            (imw, imh) = image.size
            if (imw > width) or (imh > height):
                image.thumbnail(size, Image.ANTIALIAS)

            # If RGBA, convert transparency
            if image.mode == "RGBA":
                image.load()
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background

            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=60)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output,
                                              'ImageField', "%s.jpg" %
                                              self.photo.name.split('.')[0],
                                              'image/jpeg', output.len, None)

        try:
            MyContacts.objects.get(id=self.id).photo.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(MyContacts, self).save(*args, **kwargs)


class SignalProcessor(models.Model):
    model_name = models.CharField(max_length=255)
    model_entry = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s - [%s]' % (self.model_name, self.model_entry)



def delete_signal(sender, instance, **kwargs):
    if sender.__name__ != 'SignalProcessor' and sender.__name__ != 'LogEntry':
        SignalProcessor.objects.create(model_name = instance.__class__.__name__,
                                  model_entry = 'deletion',
                                  date = datetime.now()
                                  )


def save_signal(sender, instance, created, **kwargs):
    if sender.__name__ != 'SignalProcessor' and sender.__name__ != 'LogEntry':
        SignalProcessor.objects.create(model_name = instance.__class__.__name__,
                                  model_entry = 'creation' if created else 'editing',
                                  date = datetime.now()
                                  )

post_save.connect(save_signal, dispatch_uid="my_unique_identifier")
post_delete.connect(delete_signal, dispatch_uid="my_unique_identifier")



