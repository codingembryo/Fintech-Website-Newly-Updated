from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('security/', views.security, name='security'),
    path('faq/', views.faq, name='faq'),
    path('support/', views.support, name='support'),
    path('signup/', views.signup, name='signup'),
    path('profile/dashboard', views.profile_dashboard, name='dashboard'),
    
   
]

