from django.urls import path
from .views import (
    CreateTrainerView,
    ListTrainersView,
    GetTrainerView,
    UpdateTrainerView,
    DeleteTrainerView,
)

urlpatterns = [
    path('trainers/create/', CreateTrainerView.as_view(), name='create-trainer'),
    path('trainers/', ListTrainersView.as_view(), name='list-trainers'),
    path('trainers/<int:pk>/', GetTrainerView.as_view(), name='get-trainer'),
    path('trainers/<int:pk>/update/', UpdateTrainerView.as_view(), name='update-trainer'),
    path('trainers/<int:pk>/delete/', DeleteTrainerView.as_view(), name='delete-trainer'),
]
