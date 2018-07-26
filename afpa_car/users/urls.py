from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import (PasswordResetDoneView, 
                                        PasswordResetConfirmView, PasswordResetCompleteView)

from .views import CustomPasswordResetView, CustomPasswordResetConfirmView

app_name = 'users'                            

urlpatterns = [
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),
]