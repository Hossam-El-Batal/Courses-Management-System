from django.urls import path
from .views import (
    CreatePaymentView,
    ListPaymentsView,
    GetPaymentView,
    UpdatePaymentView,
    DeletePaymentView,
    PaymentReportView
)

urlpatterns = [
    path('payment/create/', CreatePaymentView.as_view(), name='create-payment'),
    path('payment/', ListPaymentsView.as_view(), name='list-payments'),
    path('payment/<int:pk>/', GetPaymentView.as_view(), name='get-payment'),
    path('payment/<int:pk>/update/', UpdatePaymentView.as_view(), name='update-payment'),
    path('payment/<int:pk>/delete/', DeletePaymentView.as_view(), name='delete-payment'),
    path('payment-report/', PaymentReportView.as_view(), name='payment-report'),
]

