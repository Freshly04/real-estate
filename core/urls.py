from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add-item/", views.add_item, name="add-item"),
    path("detail/<int:pk>/", views.item_detail, name="detail"),
    path("update-product/<int:pk>/", views.update_item, name="update-product"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
