from django.urls import path

from klimaat_helpdesk.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    create_user)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("create/", view=create_user, name="create-user"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
