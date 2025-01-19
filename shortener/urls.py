from django.urls import path
from . import views

urlpatterns = [
    path('shorten/', views.shorten_urls, name='shorten_url'),
    path('r/<str:short_url>/', views.redirect_url, name='redirect_url'),
    path('analytics/<str:short_url>/', views.get_analytics, name='get_analytics'),
]

