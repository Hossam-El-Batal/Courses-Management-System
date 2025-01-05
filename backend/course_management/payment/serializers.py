from rest_framework import serializers
from .models import Payment, CourseTrainerHours


class CourseTrainerHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTrainerHours
        fields = ['trainer', 'course', 'hours_worked']


class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'trainer', 'course', 'hours_worked', 'payment_date', 'status', 'amount']

    def create(self, validated_data):
        trainer = validated_data.get('trainer')
        course = validated_data.get('course')
        hours_worked = validated_data.get('hours_worked')
        payment_date = validated_data.get('payment_date')
        status = validated_data.get('status')

        if hours_worked is None:
            raise serializers.ValidationError({"hours_worked": "This field cannot be null"})

        payment = Payment.objects.create(
            trainer=trainer,
            course=course,
            hours_worked=hours_worked,
            payment_date=payment_date,
            status=status
        )

        return payment

