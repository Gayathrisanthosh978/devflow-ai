from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.pagination import DefaultPagination
from apps.projects.models import Project

from .models import Task, TaskAttachment, TaskComment
from .permissions import CanManageTaskComments, CanManageTasks
from .serializers import (TaskAttachmentSerializer,
                          TaskAttachmentUploadSerializer,
                          TaskCommentCreateSerializer, TaskCommentSerializer,
                          TaskCommentUpdateSerializer, TaskCreateSerializer,
                          TaskSerializer, TaskUpdateSerializer)
from .services import TaskAttachmentService, TaskCommentService, TaskService


class TaskListCreateAPIView(APIView):

    permission_classes = [CanManageTasks]
    pagination_class = DefaultPagination

    def get(self, request, organization_id, project_id):

        project = get_object_or_404(
            Project,
            id=project_id,
            organization_id=organization_id,
        )

        tasks = TaskService.list_tasks(
            project=project,
            filters=request.query_params,
        )

        serializer = TaskSerializer(
            tasks,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, organization_id, project_id):

        project = get_object_or_404(
            Project,
            id=project_id,
            organization_id=organization_id,
        )

        serializer = TaskCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        task = TaskService.create_task(
            project=project,
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED,
        )


class TaskDetailAPIView(APIView):

    permission_classes = [CanManageTasks]
    pagination_class = DefaultPagination

    def get(self, request, task_id):

        task = get_object_or_404(
            Task,
            id=task_id,
        )

        return Response(TaskSerializer(task).data)

    def patch(self, request, task_id):

        task = get_object_or_404(
            Task,
            id=task_id,
        )

        serializer = TaskUpdateSerializer(
            task,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        task = TaskService.update_task(
            task=task,
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(TaskSerializer(task).data)

    def delete(self, request, task_id):

        task = get_object_or_404(
            Task,
            id=task_id,
        )

        TaskService.delete_task(
            task=task,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCommentListCreateAPIView(APIView):

    permission_classes = [CanManageTasks]
    pagination_class = DefaultPagination

    def get(self, request, task_id):

        task = get_object_or_404(
            Task,
            id=task_id,
        )

        comments = TaskCommentService.list_comments(
            task=task,
        )

        serializer = TaskCommentSerializer(
            comments,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, task_id):

        task = get_object_or_404(
            Task,
            id=task_id,
        )

        serializer = TaskCommentCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        comment = TaskCommentService.create_comment(
            task=task,
            user=request.user,
            comment=serializer.validated_data["comment"],
        )

        return Response(
            TaskCommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )


class TaskCommentDetailAPIView(APIView):

    permission_classes = [CanManageTaskComments]
    pagination_class = DefaultPagination

    def patch(self, request, comment_id):

        comment = get_object_or_404(
            TaskComment,
            id=comment_id,
        )

        serializer = TaskCommentUpdateSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        comment = TaskCommentService.update_comment(
            task_comment=comment,
            comment=serializer.validated_data["comment"],
        )

        return Response(TaskCommentSerializer(comment).data)

    def delete(self, request, comment_id):

        comment = get_object_or_404(
            TaskComment,
            id=comment_id,
        )

        TaskCommentService.delete_comment(
            task_comment=comment,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskAttachmentListCreateAPIView(APIView):

    permission_classes = [CanManageTasks]
    pagination_class = DefaultPagination

    def get(self, request, task_id):

        task = get_object_or_404(
            Task,
            id=task_id,
        )

        attachments = TaskAttachmentService.list_attachments(
            task=task,
        )

        serializer = TaskAttachmentSerializer(
            attachments,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, task_id):

        task = get_object_or_404(
            Task,
            id=task_id,
        )

        serializer = TaskAttachmentUploadSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        attachment = TaskAttachmentService.upload_attachment(
            task=task,
            uploaded_by=request.user,
            file=serializer.validated_data["file"],
        )

        return Response(
            TaskAttachmentSerializer(attachment).data,
            status=status.HTTP_201_CREATED,
        )


class TaskAttachmentDetailAPIView(APIView):

    permission_classes = [CanManageTasks]
    pagination_class = DefaultPagination

    def delete(self, request, attachment_id):

        attachment = get_object_or_404(
            TaskAttachment,
            id=attachment_id,
        )

        TaskAttachmentService.delete_attachment(
            attachment=attachment,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
