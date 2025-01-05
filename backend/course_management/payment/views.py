from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Payment, CourseTrainerHours
from .serializers import PaymentSerializer, CourseTrainerHoursSerializer
from django.db.models import Sum, F
from datetime import datetime


class CreatePaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPaymentsView(APIView):
    def get(self, request):
        payments = Payment.objects.all().select_related('trainer', 'course')

        # filter by date ..optional
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            payments = payments.filter(payment_date__range=[start_date, end_date])

        # filtering by trainer..optional
        trainer_id = request.query_params.get('trainer_id')
        if trainer_id:
            payments = payments.filter(trainer_id=trainer_id)

        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class GetPaymentView(APIView):
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)


class UpdatePaymentView(APIView):
    def put(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePaymentView(APIView):
    def delete(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentReportView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        payments = Payment.objects.all()

        if start_date and end_date:
            payments = payments.filter(payment_date__range=[start_date, end_date])

        summary = {
            'total_payments': payments.count(),
            'total_amount': payments.aggregate(total=Sum('amount'))['total'] or 0,
            'total_hours': payments.aggregate(total=Sum('hours_worked'))['total'] or 0,
            'pending_payments': payments.filter(status='PENDING').count(),
            'paid_payments': payments.filter(status='PAID').count(),

            'trainer_summary': list(payments.values(
                'trainer__name'
            ).annotate(
                total_amount=Sum('amount'),
                total_hours=Sum('hours_worked')
            )),

            'course_summary': list(payments.values(
                'course__title'
            ).annotate(
                total_amount=Sum('amount'),
                total_hours=Sum('hours_worked')
            ))
        }

        return Response(summary)