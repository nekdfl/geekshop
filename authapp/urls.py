from django.urls import path

from authapp.views import LoginTemplateView, RegisterUser, Profile, Logout

app_name = "authapp"
urlpatterns = [
    path('login/', LoginTemplateView.as_view(), name="login"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('profile/', Profile.as_view(), name="profile"),
    path('logout/', Logout.as_view(), name="logout"),
    path('verify/<str:email>/<str:activate_key>/', RegisterUser.verify, name='verify'),
]
