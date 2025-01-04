from django.urls import path
from .views import (
    CreateCourseView,
    ListCoursesView,
    GetCourseView,
    UpdateCourseView,
    DeleteCourseView,
    AssignTrainerToCourseView
)

urlpatterns = [
    path('courses/', ListCoursesView.as_view(), name='list-courses'),
    path('courses/create/', CreateCourseView.as_view(), name='create-course'),
    path('courses/<int:pk>/', GetCourseView.as_view(), name='get-course'),
    path('courses/<int:pk>/update/', UpdateCourseView.as_view(), name='update-course'),
    path('courses/<int:pk>/delete/', DeleteCourseView.as_view(), name='delete-course'),
    path('courses/<int:pk>/assign-trainer/', AssignTrainerToCourseView.as_view(), name='assign-trainer'),

]