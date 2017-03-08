from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.middleware.csrf import rotate_token

def index(request):
    """
    Generate the template info so we can serve the front end.
    """

    return render(request, 'index.tpl.html')

@api_view(['GET'])
@permission_classes(())
def healthcheck(request):
    """
    Health check for elastic beanstalk
    """

    return Response({'PONG!!!!'})

@api_view(['GET'])
def generateCSRF(request):
    """
    Endpoint to generate CSRF token
    """
    rotate_token(request)
    return Response({'csrf': request.META['CSRF_COOKIE'], 'status': 200})