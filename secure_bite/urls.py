from django.urls import path
from secure_bite import views

app_name = "secure_bite"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('user/', views.UserDetails.as_view(), name="user"),
    path("protected/", views.ProtectedView.as_view(), name="protected"),
]
