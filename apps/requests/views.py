from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from django.views.generic import View
from django.http import HttpResponse
from .models import Request

'''
    all_requests = Request.objects.all()
    if all_requests.count() > 10:
        q = all_requests.order_by('-date')[0:10]
        l = [i.id for i in q]
        for x in all_requests:
            if x.id not in l:
                Request.objects.filter(id=x.id).delete()
        ten_request = all_requests.order_by('-date')
    else:
        ten_request = all_requests.order_by('-date')
'''

def requests(request):
    return render_to_response('requests/requests.html', {'ten_request': Request.objects.all().order_by('-priority', '-date')[0:10]}, context_instance=RequestContext(request))



class AjaxRequests(View):

    def get(self, request):
        ten_request = Request.objects.all().order_by('-priority', '-date')[0:10]
        new_requests_count = len([new_request for new_request in ten_request
                                  if not new_request.viewed])

        requests_to_json = [{'date': request.date.strftime('%A, %H:%M, %d-%m-%Y'),
                             'method': request.method,
                             'path': request.path,
                             'server_protocol': request.server_protocol,
                             'ip_addr': request.ip_addr,
                             'viewed': request.viewed,
                             'id': request.id,
                             'priority': request.priority,}
                            for request in ten_request]
        return HttpResponse(json.dumps({'ajaxrequests': requests_to_json,
                                        'new_requests': new_requests_count}),
                            content_type="application/json")

    def post(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            for request_data in data:
                if request_data['viewed']:
                    continue
                request_objects = Request.objects.all().filter(id=request_data['id'])
                for request_object in request_objects:
                    request_object.viewed = True
                    request_object.save()
            else:
                return HttpResponse(json.dumps({'success': True}),
                                    content_type="application/json")
        return HttpResponse(json.dumps({'success': False}),
                            content_type="application/json")

