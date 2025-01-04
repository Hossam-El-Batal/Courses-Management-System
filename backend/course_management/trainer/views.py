from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trainer
from .serializers import TrainerSerializer
from django.shortcuts import get_object_or_404


class CreateTrainerView(APIView):

    def post(self, request):
        if request.method == "POST":
            serialized_data = TrainerSerializer(data=request.data)

            if serialized_data.is_valid():
                serialized_data.save()
                return Response(serialized_data.data, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)


class ListTrainersView(APIView):
    def get(self, request):
        trainers = Trainer.objects.all()
        serializer = TrainerSerializer(trainers, many=True)
        return Response(serializer.data)

class GetTrainerView(APIView):
    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        serializer = TrainerSerializer(trainer)
        return Response(serializer.data)

class UpdateTrainerView(APIView):
    def put(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        serializer = TrainerSerializer(trainer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTrainerView(APIView):
    def delete(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        trainer.delete()
        return Response({"message": "Trainer Deleted"},status=status.HTTP_204_NO_CONTENT)





