import os
import requests
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import LoanScenario
from .serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    """
    A viewset for creating and editing loan instances.
    """
    queryset = LoanScenario.objects.all().order_by('-created_at')
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        """
        Save the loan instance and calculate payments.
        """
        loan = serializer.save()
        self.calculate_payments(loan)

    def perform_update(self, serializer):
        """Update the loan instance and recalculate payments."""
        loan = serializer.save()
        self.calculate_payments(loan)

    @staticmethod
    def calculate_payments(loan):
        """
        Calculate the loan payments using the API Ninjas mortgage calculator.
        """
        logger.debug('calculating payments for loan: %s', loan.id)
        try:
            payments = get_mortgage_payments(
                loan_amount=loan.purchase_price - loan.down_payment,
                interest_rate=loan.interest_rate,
                term_in_months=loan.mortgage_term
            )

            # Update the loan instance with payment details
            loan.total_loan_amount = payments['loan_amount']
            loan.monthly_payment = payments['monthly_payment']
            loan.total_amount_paid = payments['total_paid']
            loan.total_interest_paid = payments['total_interest']
            loan.save()
        except Exception as e:
            logger.error(f"Error calculating payments for LoanScenario {loan.id}: {e}")
            raise ValidationError({"detail": "Failed to calculate loan payments. Please try again later."})
