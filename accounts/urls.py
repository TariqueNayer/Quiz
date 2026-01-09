from django.urls import path, include
from .views import ProfileView, CustomPasswordChangeView, PasswordChangeDone

urlpatterns = [
	path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
	path('password/done/', PasswordChangeDone.as_view(), name='password_change_done'),
	path('profile/', ProfileView.as_view(), name='profile'),
	path('', include("allauth.urls")),
]