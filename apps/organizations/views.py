from django.shortcuts import get_object_or_404, render
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization, OrganizationMember, OrganizationRole
from .permissions import IsOrganizationOwnerOrAdmin
from .serializers import (InviteMemberSerializer, OrganizationMemberSerializer,
                          OrganizationSerializer, UpdateMemberRoleSerializer)
from .services import OrganizationService


class OrganizationCreateView(generics.CreateAPIView):
    serializer_class = OrganizationSerializer

    def perform_create(self, serializer):
        organization = OrganizationService.create_organization(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )
        serializer.instance = organization


class OrganizationMembersAPIView(APIView):

    permission_classes = [IsOrganizationOwnerOrAdmin]

    def get(self, request, organization_id):

        organization = Organization.objects.get(id=organization_id)

        members = OrganizationService.list_members(organization=organization)

        serializer = OrganizationMemberSerializer(
            members,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, organization_id):

        organization = get_object_or_404(
            Organization,
            id=organization_id,
        )

        serializer = InviteMemberSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        OrganizationService.invite_member(
            organization=organization,
            invited_user=serializer.validated_data["email"],
            role=serializer.validated_data["role"],
        )

        return Response(
            {"detail": "Member invited successfully."},
            status=status.HTTP_201_CREATED,
        )


class OrganizationMemberDetailAPIView(APIView):

    permission_classes = [IsOrganizationOwnerOrAdmin]

    def patch(self, request, organization_id, member_id):

        organization = get_object_or_404(
            Organization,
            id=organization_id,
        )

        member = get_object_or_404(
            OrganizationMember,
            id=member_id,
            organization=organization,
        )

        serializer = UpdateMemberRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if member.role == OrganizationRole.OWNER:
            return Response(
                {"detail": "Owner role cannot be changed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        OrganizationService.update_member_role(
            member=member,
            role=serializer.validated_data["role"],
        )

        return Response({"detail": "Member role updated successfully."})

    def delete(self, request, organization_id, member_id):

        organization = get_object_or_404(
            Organization,
            id=organization_id,
        )

        member = get_object_or_404(
            OrganizationMember,
            id=member_id,
            organization=organization,
        )

        if member.role == OrganizationRole.OWNER:
            return Response(
                {"detail": "Owner cannot be removed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        OrganizationService.remove_member(member=member)

        return Response(
            {"detail": "Member removed successfully."},
            status=status.HTTP_200_OK,
        )
