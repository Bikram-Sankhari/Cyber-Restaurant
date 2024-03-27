from . import models
from vendor import models as vendor_models

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        models.request_from_middleware = request
        vendor_models.REQUEST_FROM_MIDDLEWARE = request


        response = self.get_response(request)


        return response