from django.test import TestCase
from apps.requests.models import Request
import datetime
import json


class MiddlewareTest(TestCase):

    def test_middleware(self):
        self.client.get('/')
        response = self.client.get('/requests/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Request.objects.count(), 2)


class RequestsModelTest(TestCase):
    def setUp(self):
        for i in range(20, 40):
            Request.objects.create(date=datetime.datetime.now(), method='POST', path='/', server_protocol='HTTP/1.1', ip_addr='31.215.125.%d'%(i), viewed=False)

    def test_requests(self):
        response = self.client.get('/requests/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Request.objects.count(), 21)
        self.assertContains(response, 'requests')
        for i in range(31, 40):
            self.assertContains(response, '31.215.125.%d'%(i))

    def test_ajax(self):
        response = self.client.post('/requests/ajaxrequests/', {'data': json.dumps([{'id': 1, 'viewed': False}, {'id': 2, 'viewed': True}])}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(Request.objects.filter(viewed=True).count(), 1)

class PriorityTest(TestCase):
    def setUp(self):
        for i in range(20, 40):
            Request.objects.create(date=datetime.datetime.now(), method='POST', path='/', server_protocol='HTTP/1.1', ip_addr='31.215.125.%d'%(i), viewed=False)

    def test_priority(self):
        for i in range(1, 11):
            Request.objects.create(date=datetime.datetime.now(), method='POST', path='/', server_protocol='HTTP/1.1', ip_addr='31.215.125.%d'%(i), viewed=False, priority=0)
        response = self.client.get('/requests/')
        self.assertNotContains(response, '<td>0</td>')


        
