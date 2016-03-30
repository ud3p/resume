from .models import MyContacts
from django import forms


class MyContactsModelForm(forms.ModelForm):
    class Meta:
        model = MyContacts
        #fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class':'datepicker'}),
        }


    #date_of_birth = forms.DateField(widget=DateInput)

