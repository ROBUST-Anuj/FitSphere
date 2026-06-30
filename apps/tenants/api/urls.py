from django.urls import path

from apps.tenants.api.views import MembershipCreateAPIView, MembershipListAPIView

app_name = "tenants"

urlpatterns = [
    path(
        "members/",
        MembershipListAPIView.as_view(),
        name="member-list",
    ),
    path(
        "members/add/",
        MembershipCreateAPIView.as_view(),
        name="member-add",
    ),
]
