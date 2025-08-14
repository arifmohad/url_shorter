import random, string
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import URL
from .serializers import URLSerializer
import re
from rest_framework import status
def home(request):
    return render(request, 'index.html')

def redirect_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)

def is_valid_url(url):
    # Simple URL regex validation
    url_pattern = re.compile(
        r'^(http|https)://'  # must start with http:// or https://
        r'([a-zA-Z0-9.-]+)'  # domain
        r'(:[0-9]+)?'        # optional port
        r'(\/.*)?$'          # optional path
    )
    return bool(url_pattern.match(url))

@api_view(['POST'])
def create_short_url(request):
    original_url = request.data.get('url')

    # Validate if provided URL is in correct format
    if not original_url or not is_valid_url(original_url):
        return Response(
            {"error": "Invalid URL format. Must start with http:// or https://"},
            status=status.HTTP_400_BAD_REQUEST
        )

    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    url_obj = URL.objects.create(original_url=original_url, short_code=short_code)
    serializer = URLSerializer(url_obj)
    return Response(serializer.data)