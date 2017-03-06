from django.shortcuts import render
from rest_framework.response import Response

def index(request):
    """
    Generate the template info so we can serve the front end.
    """

    return render(request, 'index.tpl.html')

def healthcheck(request):
    """
    Health check for elastic beanstalk
    """

    return Response({'PONG!!!!'})
