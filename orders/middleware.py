from . import models

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        models.request_from_middleware = request

        response = self.get_response(request)


        return response