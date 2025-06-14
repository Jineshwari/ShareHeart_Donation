from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),              # Home page
    path('home2/', views.home2, name='home2'),
    path('about/', views.about, name='about'),      # About page
    path('contact/', views.contact, name='contact'), # Contact page
    path('donate/', views.donate, name='donate'),   # Donate page
    path('donate2/', views.donate2, name='donate2'), # Donate2 page
    path('donate3/', views.donate3, name='donate3'), # Donate3 page
    path('rewards/', views.rewards, name='rewards'), # Donate3 page
    path('ngo_login/', views.ngo_login, name='ngo_login'),
    path('user_login/', views.user_login, name='user_login'),
    path('ngo_register/', views.ngo_register, name='ngo_register'),
    path('user_register/', views.user_register, name='user_register'),
    path('account/', views.account, name='account'),
    path('success/', views.success_view, name='success_url'),  # A view to show success message


    # Catch-all pattern for any undefined URLs
    path('<str:page>/', views.dynamic_page, name='dynamic_page'), 
]
