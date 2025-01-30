import decimal

from django import forms
from .models import LoanScenario


class LoanForm(forms.ModelForm):
    template_name = 'mortgage/loan_form_inner.html'
    down_payment_value = forms.IntegerField(
        label='Down Payment Value',
        help_text='Enter the down payment value',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 20'})
    )
    down_payment_type = forms.ChoiceField(
        label='Down Payment Type',
        choices=[('percent', '%'), ('amount', '$')],
        widget=forms.RadioSelect
    )
    mortgage_term_value = forms.IntegerField(
        label='Mortgage Term Value',
        help_text='Enter the mortgage term value',
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 30'})
    )
    mortgage_term_unit = forms.ChoiceField(
        label='Mortgage Term Unit',
        choices=[('years', 'Years'), ('months', 'Months')],
        widget=forms.RadioSelect
    )

    class Meta:
        model = LoanScenario
        fields = ['purchase_price',
                  'interest_rate',
                  'down_payment_value',
                  'down_payment_type',
                  'mortgage_term_value',
                  'mortgage_term_unit',
                  'monthly_payment',
                  'total_amount_paid',
                  'total_interest_paid']

    def save(self, commit=True):
        loan = super().save(commit=False)

        down_payment_value = self.cleaned_data['down_payment_value']
        down_payment_type = self.cleaned_data['down_payment_type']
        mortgage_term_value = self.cleaned_data['mortgage_term_value']
        mortgage_term_unit = self.cleaned_data['mortgage_term_unit']

        # Calculate down_payment in dollars
        if down_payment_type == 'percent':
            loan.down_payment = decimal.Decimal(down_payment_value / 100) * loan.purchase_price
        else:
            loan.down_payment = down_payment_value

        # Normalize mortgage_term to months
        if mortgage_term_unit in ['year', 'years']:
            loan.mortgage_term = mortgage_term_value * 12
        else:
            loan.mortgage_term = mortgage_term_value

        if loan.mortgage_term < 12:
            raise forms.ValidationError("Mortgage term must be at least 12 months.")

        if commit:
            loan.save()
        return loan
