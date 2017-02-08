"""silo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import SimpleRouter

# Views
from silo import views as index_view
from messagesapp import views as messages_views
from contacts import views as contacts_views

ROUTER = SimpleRouter()

# Messages
ROUTER.register(
    r'messages',
    messages_views.MessagesView,
    base_name='messages'
)
ROUTER.register(
    r'receive/messages',
    messages_views.ReceiveMessagesView,
    base_name='receive_messages')

# User
ROUTER.register(
    r'user',
    contacts_views.GetUserInfoView,
    base_name="user_info")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/', include(ROUTER.urls, namespace='api')),
    # url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login')
]

urlpatterns += [
    # Do NOT return 200 for missing API calls.
    url(r'^(?!api/)', index_view.index, name="index"),
    # url(r'^accounts/', include('allauth.urls')),
]
