from django.db import models


class Loan(models.Model):
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    mortgage_term = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    total_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_interest_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Loan {self.id}"
