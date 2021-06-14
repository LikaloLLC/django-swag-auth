from django.http import JsonResponse


def complete_authentication(request, token):
    return JsonResponse(status=200, data={'token': token.id})
