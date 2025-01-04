from rest_framework import serializers
from .models import Course
from trainer.serializers import TrainerSerializer
from trainer.models import Trainer


class CourseSerializer(serializers.ModelSerializer):
    trainer_details = TrainerSerializer(source='trainer', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("End date must be after start date")
        return data


class CourseTrainerAssignmentSerializer(serializers.Serializer):
    trainer_id = serializers.IntegerField()

    def validate_trainer_id(self, value):
        try:
            Trainer.objects.get(pk=value)
            return value
        except Trainer.DoesNotExist:
            raise serializers.ValidationError("Invalid trainer ID")
