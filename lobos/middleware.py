from django.conf import settings

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        print(get_response)
        pass

    # stopped on 26


