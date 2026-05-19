from django.urls import path
from . views import *

urlpatterns = [
    path('', index, name = "home-page"),
    path('register', signup, name = "sign-up"),
    path('login',signin, name = "sign-in"),
    path('logout', signout, name = "sign-out"),
    path('submit_item',submititems, name = "submit-item"),
    path('mypost',mypost, name = "my-posts"),
    path('allitems', allitems, name = "all-items"),
    path('mark-found/<int:pk>/', mark_found, name='mark-found'),
    path('delete/<int:pk>/', delete_item, name='delete-item'),
]