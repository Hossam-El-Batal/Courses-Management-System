from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment, CourseTrainerHours
from .serializers import PaymentSerializer, CourseTrainerHoursSerializer
from django.db.models import Sum, F
from datetime import datetime
from django.shortcuts import render
from .models import Payment, Trainer, Course
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreatePaymentView(APIView):

    def get(self, request):
        trainers = Trainer.objects.all()
        courses = Course.objects.all()
        return render(request, 'payments/create_payment.html', {
            'trainers': trainers,
            'courses': courses
        })

    def post(self, request):
        print(request.data)
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return redirect('list-payments')
        return render(request, 'payments/create_payment.html', {
                'errors': serializer.errors,
                'trainers': Trainer.objects.all(),
                'courses': Course.objects.all()
            })


class ListPaymentsView(APIView):

    def get(self, request):
        payments = Payment.objects.all().select_related('trainer', 'course')

        # Filter logic
        filters = {}
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        trainer_id = request.GET.get('trainer_id')
        status_filter = request.GET.get('status')

        if start_date and end_date:
            filters['payment_date__range'] = [start_date, end_date]
        if trainer_id:
            filters['trainer_id'] = trainer_id
        if status_filter:
            filters['status'] = status_filter

        payments = payments.filter(**filters).order_by('-payment_date')

        context = {
            'payments': payments,
            'trainers': Trainer.objects.all(),
            'filters': {
                'start_date': start_date,
                'end_date': end_date,
                'trainer_id': trainer_id,
                'status': status_filter
            }
        }
        return render(request, 'payments/list_payments.html', context)


class GetPaymentView(APIView):

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment)
        return render(request, 'payments/payment_detail.html', {'payment': payment})


class UpdatePaymentView(APIView):

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        trainers = Trainer.objects.all()
        courses = Course.objects.all()
        return render(request, 'payments/payment_update.html', {
            'payment': payment,
            'trainers': trainers,
            'courses': courses
        })

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            payment = serializer.save()
            # doing recalculation for amount
            payment.amount = payment.calculate_payment()
            payment.save()
            return redirect('list-payments')
        return render(request, 'payments/payment_update.html', {
            'payment': payment,
            'errors': serializer.errors,
            'trainers': Trainer.objects.all(),
            'courses': Course.objects.all()
        })


class DeletePaymentView(APIView):

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        return render(request, 'payments/payment_confirm_delete.html', {'payment': payment})

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return redirect('list-payments')


class PaymentReportView(APIView):

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        trainer_id = request.GET.get('trainer_id')

        payments = Payment.objects.all()
        filters = {}

        if start_date and end_date:
            filters['payment_date__range'] = [start_date, end_date]
        if trainer_id:
            filters['trainer_id'] = trainer_id

        payments = payments.filter(**filters)

        summary = {
            'total_payments': payments.count(),
            'total_amount': payments.aggregate(total=Sum('amount'))['total'] or 0,
            'total_hours': payments.aggregate(total=Sum('hours_worked'))['total'] or 0,
            'pending_payments': payments.filter(status='PENDING').count(),
            'paid_payments': payments.filter(status='PAID').count(),
            'trainer_summary': payments.values(
                'trainer__name'
            ).annotate(
                total_amount=Sum('amount'),
                total_hours=Sum('hours_worked')
            ).order_by('-total_amount'),
            'course_summary': payments.values(
                'course__title'
            ).annotate(
                total_amount=Sum('amount'),
                total_hours=Sum('hours_worked')
            ).order_by('-total_amount')
        }

        context = {
            'summary': summary,
            'trainers': Trainer.objects.all(),
            'filters': {
                'start_date': start_date,
                'end_date': end_date,
                'trainer_id': trainer_id
            }
        }
        return render(request, 'payments/payment_report.html', context)
