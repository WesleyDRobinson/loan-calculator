import os
import requests
from rest_framework import viewsets
from .models import Loan
from .serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        loan = serializer.save()
        self.calculate_payments(loan)

    def perform_update(self, serializer):
        loan = serializer.save()
        self.calculate_payments(loan)

    def calculate_payments(self, loan):
        # Call API Ninjas mortgage calculator
        response = requests.get(
            'https://api.api-ninjas.com/v1/mortgagecalculator',
            params={
                'loan_amount': loan.purchase_price - loan.down_payment,
                'interest_rate': loan.interest_rate,
                'term': loan.mortgage_term
            },
            headers={'X-Api-Key': os.getenv('API_NINJAS_KEY')}
        )

        data = response.json()
        loan.total_loan_amount = data['loan_amount']
        loan.monthly_payment = data['monthly_payment']
        loan.total_amount_paid = data['total_amount_paid']
        loan.total_interest_paid = data['total_interest_paid']
        loan.save()
