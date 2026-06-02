from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from doctors.views import medecin_signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('doctors/', include('doctors.urls')),  # Toutes les URLs de doctors
    path('doctors/signup/', medecin_signup, name='medecin_signup'),  # La route directe pour le signup
    path('appointments/', include('appointments.urls')),
    path('ai/', include('ai_orientation.urls')),
    path('notifications/', include('notifications.urls')),
    path('schedules/', include('schedules.urls')),
    path('mot-de-passe/', include([
        path('reinitialiser/', auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            success_url='/mot-de-passe/reinitialiser/envoye/'
        ), name='password_reset'),
        path('reinitialiser/envoye/', auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ), name='password_reset_done'),
        path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url='/mot-de-passe/reinitialiser/termine/'
        ), name='password_reset_confirm'),
        path('reinitialiser/termine/', auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ), name='password_reset_complete'),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler404 = 'accounts.views.page_404'
handler500 = 'accounts.views.page_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


