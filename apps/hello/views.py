import json
from django.shortcuts import render, render_to_response
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.shortcuts import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from .models import MyContacts
from .forms import MyContactsModelForm

def index(request):
    return render(request, 'index.html', {'contact': MyContacts.objects.get(id=1)})

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {'pk': self.object.pk}
            return self.render_to_json_response(data)
        else:
            return response


class EditInfo(AjaxableResponseMixin, UpdateView):
    model = MyContacts
    template_name = 'edit.html'
    form_class = MyContactsModelForm
    success_url = reverse_lazy('index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditInfo, self).dispatch(*args, **kwargs)
'''
    def get_success_url(self):
        return reverse_lazy('edit', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        message = super(EditInfo, self).form_valid(form)
        messages.success(self.request, u'The changes have been saved.')
        return message
'''

