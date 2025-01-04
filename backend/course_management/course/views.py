from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course, Trainer
from .serializers import CourseSerializer, CourseTrainerAssignmentSerializer


class CreateCourseView(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCoursesView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class GetCourseView(APIView):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)


class UpdateCourseView(APIView):
    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCourseView(APIView):
    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignTrainerToCourseView(APIView):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseTrainerAssignmentSerializer(data=request.data)

        if serializer.is_valid():
            trainer = get_object_or_404(Trainer, pk=serializer.validated_data['trainer_id'])
            course.trainer = trainer
            course.save()

            response_serializer = CourseSerializer(course)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.trainer = None
        course.save()

        response_serializer = CourseSerializer(course)
        return Response(response_serializer.data)
