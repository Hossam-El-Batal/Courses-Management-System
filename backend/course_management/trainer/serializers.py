from rest_framework import serializers

from trainer.models import Trainer


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Invalid Phone Number")
        return value

    def validate_hourly_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError("Hourly rate must be greater than zero")
        return value
