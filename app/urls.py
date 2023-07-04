from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login_view, name="login_view"),
    path('register_view/',views.register_view, name="register_view"),
    path('posts/all/', views.all_posts, name='all_posts'),
    path('posts/create', views.create_post, name='create_post'),
    path('posts/update/<int:post_id>/',views.update_post, name='update_post'),
    path('posts/delete/<int:post_id>/',views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/',views.post_details, name='post_details'),
    path('logout/', views.logout_view, name='logout'),
]