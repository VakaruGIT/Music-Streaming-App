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
    path('music/upload/', views.upload_music_track, name='music_upload'), # DONE
    path('music/edit/<int:music_track_id>/', views.music_edit, name='music_edit'),
    path('music/delete/<int:music_track_id>/', views.music_delete, name='music_delete'),
    path('music/search/', views.music_search_page, name='music_search'),
    path("music/search/results/", views.music_search_results, name="music_search_results"),

    # path('music/search/', views.music_search_page, name='music_search'),
    #path('music/play/<int:music_track_id>/', views.music_play, name='music_play'),

]