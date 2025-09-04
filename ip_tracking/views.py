from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ratelimit.decorators import ratelimit


# Anonymous users: 5/minute
@ratelimit(key='ip', rate='5/m', block=True)
def public_view(request):
    return JsonResponse({"message": "Public access granted"})


# Authenticated users: 10/minute
@login_required
@ratelimit(key='ip', rate='10/m', block=True)
def login_view(request):
    return JsonResponse({"message": "Login successful"})
