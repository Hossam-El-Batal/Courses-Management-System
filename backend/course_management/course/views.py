from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course, Trainer
from .serializers import CourseSerializer, CourseTrainerAssignmentSerializer


class CreateCourseView(APIView):

    def get(self, request):
        return render(request, 'courses/create_course.html')
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('list-courses')
        return render(request, 'courses/create_course.html')


class ListCoursesView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return render(request, 'courses/list_courses.html', {'courses': courses})


class GetCourseView(APIView):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return render(request, 'courses/get_course.html', {'course': course})

class UpdateCourseView(APIView):

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        return render(request, 'courses/update_course.html', {'course': course})

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.POST)

        if serializer.is_valid():
            serializer.save()
            return redirect('get-course', pk=pk)
        return render(request, 'courses/update_course.html', {'course': course})

class DeleteCourseView(APIView):

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        return render(request, 'courses/delete_course.html', {'course': course})

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if request.POST.get('_method') == 'DELETE':
            course.delete()
            return redirect('list-courses')
        return redirect('list-courses')


class AssignTrainerToCourseView(APIView):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        trainers = Trainer.objects.all()
        return render(request, 'courses/assign_trainer.html', {'course': course, 'trainers': trainers})

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        # Handle unassigning
        if 'unassign' in request.POST:
            course.trainer = None
            course.save()
            return redirect('get-course', pk=pk)

        # Handle assigning
        trainer_id = request.POST.get('trainer_id')
        if trainer_id:
            trainer = get_object_or_404(Trainer, pk=trainer_id)
            course.trainer = trainer
            course.save()
            return redirect('get-course', pk=pk)

        # If no valid action
        trainers = Trainer.objects.all()
        return render(request, 'courses/assign_trainer.html', {'course': course, 'trainers': trainers, 'error': 'Invalid action'})
