from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.register, name='register'), #DONE
    path('login/', views.login, name='login'), #DONE
    path('logout/', LogoutView.as_view(next_page ="register"), name='logout'), #DONE
    path("home/", views.home_page, name="home-page"), #DONE
    path("profile/", views.profile, name="profile"), #DONE
    path("music/", views.music_page, name="music_page"), #DONE
    #path('music/search/', views.music_search_page, name='music_search'),

    path('music/upload/', views.music_upload, name='music_upload'),

    #path('music/play/<int:music_track_id>/', views.music_play, name='music_play'),

]