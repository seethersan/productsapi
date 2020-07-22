from django.views.generic import View
from django.http import HttpResponse

# Create your views here.
class HealthCheck(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=200) 