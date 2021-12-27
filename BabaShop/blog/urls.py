from django.urls import path
from blog.views import PostListView, PostDetail, Register_site, add_category, add_comment, add_post, add_tag, change_password, contact_site,\
                    delete_category, delete_post, each_category_posts, each_tag_posts, each_user_posts, edit_post, login_site, logout_site,\
                    search_site, show_category_list, show_tag_list, edit_category, delete_tag, edit_tag

urlpatterns = [
    path('post-list/', PostListView.as_view(), name='post-list'),
    path('post-detail/<slug:slug>', PostDetail.as_view(), name='post_detail'),
    path('category-list/', show_category_list, name='category-list'),
    path('category-posts/<int:id>', each_category_posts, name = 'category_to_posts'),
    path('tag-list/', show_tag_list, name='tag-list'),
    path('tag-posts/<int:id>', each_tag_posts, name = 'tag_to_posts'),

    path('login/', login_site, name='login_url'),
    path('logout/', logout_site, name='logout_url'),
    path('register/', Register_site, name='register_url'),
    path('changepassword/', change_password, name='change_password_url'),

    path('add_category/', add_category, name='add_category_url'),
    path('add_tag/', add_tag, name='add_tag_url'),
    path('delete_category/<int:id>',delete_category, name="delete_category_url"),
    path('edit_category/<int:id>',edit_category, name="edit_category_url"),
    path('delete_tag/<int:id>',delete_tag, name="delete_tag_url"),
    path('edit_tag/<int:id>',edit_tag, name="edit_tag_url"),
    path('delete_post/<slug:slug>',delete_post, name="delete_post_url"),
    path('edit_post/<slug:slug>',edit_post, name="edit_post_url"),

    path('user_posts/', each_user_posts, name='user_posts_url'),
    path('add_post/', add_post, name='add_post_url'),
    path('add_comment/<slug:slug>', add_comment, name='add_comment_url'),

    path('search/', search_site, name='search_url'),
    # path('post_like/', post_like, name='post_like_url'),
    path('contact/', contact_site, name='contact_url'),
]
