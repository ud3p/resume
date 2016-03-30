from .models import Request

class HttpRequestMiddleware(object):
    def process_request(self, request):
        if not request.is_ajax():
            data = Request()
            data.method = request.META['REQUEST_METHOD']
            data.path = request.path
            data.server_protocol = request.META['SERVER_PROTOCOL']
            data.ip_addr = request.META['REMOTE_ADDR']
            data.save()
