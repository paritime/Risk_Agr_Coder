from django.urls import path
from App_BlogAgri.views import blog, post, create_post, posts_user, edit_post, delete_post, confirm_delete


urlpatterns = [
    path('blog/', blog, name='blog'),
    path('blog/user/', posts_user, name='posts_user'),
    path('post/<slug:post_slug>/', post, name='post'),
    path('create_post/', create_post, name='create_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('confirm_delete/<int:post_id>/',
         confirm_delete, name='confirm_delete'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),

]
