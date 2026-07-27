from django.urls import path

from .views import OrganizationCreateView,OrganizationMembersAPIView,OrganizationMemberDetailAPIView

urlpatterns = [
    path("", OrganizationCreateView.as_view(), name="organization-create"),
    path("<uuid:organization_id>/members/",OrganizationMembersAPIView.as_view(), name="organization-members"),
    path("<uuid:organization_id>/members/<uuid:member_id>/", OrganizationMemberDetailAPIView.as_view(), name="organization-member-detail"),

]