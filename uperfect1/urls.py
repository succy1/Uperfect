"""
URL configuration for uperfect1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views
from product import views as product_views
from django.contrib.auth import views as auth_views
# from detection import views as detection_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_views.home, name='home'),
    path('product/', product_views.ProductListView.as_view(), name='product-list'),
    path('register/', account_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('quiz/', account_views.skin_quiz, name='quiz'),
    path('profile/', account_views.profile, name='profile'),
    path('onboarding/', account_views.onboarding, name='onboarding'),
    path('profile-completed/', product_views.profile_creation_completed, name='profile_completed'),
    path('assign-product/<int:product_id>/', product_views.assign_product, name='assign_product'),
    # path('detection/', detection_views.detect_acne, name="detect_acne"),
    path('checkin/', account_views.daily_checkin, name='daily_checkin'),
    path('pricing/', account_views.pricing, name="pricing"),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
         name='password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
