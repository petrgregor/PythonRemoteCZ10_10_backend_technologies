"""chatterbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# for images
from django.conf import settings
from django.conf.urls.static import static

import api.views
import chatterapp.views
from chatterapp.views import *
import profiles.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello, name='hello'),
    path('hello/<str:name>/', hello, name='hello2'),
    path('ahoj/', ahoj, name='ahoj'),
    path('', home, name='home'),        # empty path (home)
    path('rooms/', rooms, name='rooms'),
    path('room/<int:pk>/', room, name='room'),

    path('private_request/<int:pk>/', private_request, name='private_request'),
    path('accept_request/<int:pk>/', accept_request, name='accept_request'),
    path('deny_request/<int:pk>/', deny_request, name='deny_request'),
    path('private_requests/', private_requests, name='private_requests'),

    path('new_room/', new_room, name='new_room'),                   # 1st version for creating room
    path('create_room/', create_room, name='create_room'),          # 1st version for creating room
    path('create_room_v2/', create_room_v2, name='create_room_v2'), # 2st version for creating room
    path('create_room_v3/', RoomFormView.as_view(), name='create_room_v3'),   # 3rd version for creating room
    path('create_room_v4/', RoomCreateView.as_view(), name='create_room_v4'),  # 4rd version for creating room

    path('edit_room/<int:pk>/', chatterapp.views.EditRoom.as_view(), name='edit_room'),

    path('delete_room/<int:pk>/', delete_room, name='delete_room'),
    path('delete_room_yes/<int:pk>/', delete_room_yes, name='delete_room_yes'),

    path('search/', chatterapp.views.search, name='search'),

    # accounts app
    path('accounts/', include('accounts.urls')),             # signup
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password_change,...
    path('accounts/profile/', rooms),

    # profiles app
    path('profile/<int:pk>/', profiles.views.profile, name='profile'),
    path('create_profile/', profiles.views.create_profile, name='create_profile'),
    path('edit_profile/', profiles.views.edit_profile, name='edit_profile'),

    # api
    path('api/hello_world/', api.views.hello_world),
    path('api/rooms/', api.views.rooms),
    path('api/room/<int:pk>/', api.views.room),
    path('api/messages/<int:pk>/', api.views.messages),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
