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
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import SimpleRouter

# Views
from silo import views as index_view
from messagesapp import views as messages_views
from contacts import views as contacts_views

ROUTER = SimpleRouter()

# Messages
ROUTER.register(
    r'messages/opt',
    messages_views.OptInView,
    base_name='opt'
)
ROUTER.register(
    r'messages',
    messages_views.MessagesView,
    base_name='messages'
)
ROUTER.register(
    r'receive/messages',
    messages_views.ReceiveMessagesView,
    base_name='receive_messages')

ROUTER.register(
    r'status/messages',
    messages_views.MessagesViewStatus,
    base_name='message_status'
)


# Contacts / User views
ROUTER.register(
    r'user',
    contacts_views.GetUserInfoView,
    base_name="user_info")

ROUTER.register(
    r'contact',
    contacts_views.ContactCardView,
    base_name="contact_cards"
)

ROUTER.register(
    r'groups',
    contacts_views.GroupsViewSet,
    base_name="groups"
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/', include(ROUTER.urls, namespace='api')),
    # url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login')
]

urlpatterns += [
    # Do NOT return 200 for missing API calls.
    url(r'^(?!api/)', admin.site.urls, name="index"),
    # url(r'^accounts/', include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
