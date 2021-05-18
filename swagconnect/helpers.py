from django.http import HttpResponse


def complete_authentication(request, token):
    return HttpResponse("<h1>Success</h1>", status=200)
