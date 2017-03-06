from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

def index(request):
    """
    Generate the template info so we can serve the front end.
    """

    return render(request, 'index.tpl.html')

@api_view(['GET'])
def healthcheck(request):
    """
    Health check for elastic beanstalk
    """

    return Response({'PONG!!!!'})
