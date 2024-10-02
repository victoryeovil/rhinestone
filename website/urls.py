from django.urls import path
from .import views

urlpatterns = [
    path("", views.index_view), 
    path("contact/", views.contact_view),
    path("gallery/", views.gallery_view),
    path("login/", views.login_view),
    path("logout/", views.logout_view, name='logout'),
    path("register/", views.register_view),
 
]
