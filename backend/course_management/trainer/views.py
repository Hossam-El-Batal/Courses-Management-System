from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trainer
from .serializers import TrainerSerializer
from django.shortcuts import get_object_or_404


class CreateTrainerView(APIView):
    def get(self, request):
        return render(request, 'trainers/create_trainer.html')
    def post(self, request):
        if request.method == "POST":
            serialized_data = TrainerSerializer(data=request.data)

            if serialized_data.is_valid():
                serialized_data.save()
                return redirect('list-trainers')

        return render(request, 'trainers/create_trainer.html', {'message': 'Method not allowed'})


class ListTrainersView(APIView):
    def get(self, request):
        trainers = Trainer.objects.all()
        serializer = TrainerSerializer(trainers, many=True)
        return render(request, 'trainers/list_trainers.html', {'trainers': trainers})


class GetTrainerView(APIView):
    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        serializer = TrainerSerializer(trainer)
        return render(request, 'trainers/get_trainer.html', {'trainer': trainer})


class UpdateTrainerView(APIView):

    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        return render(request, 'trainers/update_trainer.html', {'trainer': trainer})

    def post(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        serialized_data = TrainerSerializer(trainer, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return redirect('list-trainers')
        return render(request, 'trainers/update_trainer.html', {'trainer': trainer, 'errors': serialized_data.errors})


class DeleteTrainerView(APIView):
    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        return render(request, 'trainers/delete_trainer.html', {'trainer': trainer})

    def post(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        trainer.delete()
        return redirect('list-trainers')


