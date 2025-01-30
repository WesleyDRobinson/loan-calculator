import decimal
from rest_framework import serializers
from .models import LoanScenario
import logging

logger = logging.getLogger('mortgage')


class LoanSerializer(serializers.ModelSerializer):
    down_payment_value = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    down_payment_type = serializers.ChoiceField(choices=[('percent', '%'), ('amount', '$')], write_only=True)
    mortgage_term_value = serializers.IntegerField(write_only=True)
    mortgage_term_unit = serializers.ChoiceField(choices=[('years', 'Years'), ('months', 'Months')], write_only=True)

    class Meta:
        model = LoanScenario
        fields = [
            'id',
            'purchase_price',
            'down_payment_value',
            'down_payment_type',
            'mortgage_term_value',
            'mortgage_term_unit',
            'interest_rate',
            'total_loan_amount',
            'monthly_payment',
            'total_amount_paid',
            'total_interest_paid',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'total_loan_amount',
            'monthly_payment',
            'total_amount_paid',
            'total_interest_paid',
            'created_at',
            'updated_at',
        ]

    @staticmethod
    def validate_purchase_price(value):
        if value <= 0:
            raise serializers.ValidationError("Purchase price must be a positive number.")
        return value

    @staticmethod
    def validate_down_payment_value(value):
        if value < 0:
            raise serializers.ValidationError("Down payment value cannot be negative.")
        return value

    @staticmethod
    def validate_mortgage_term_value(value):
        if value <= 0:
            raise serializers.ValidationError("Mortgage term value must be a positive integer.")
        return value

    def create(self, validated_data):
        down_payment_value = validated_data.pop('down_payment_value')
        down_payment_type = validated_data.pop('down_payment_type')
        mortgage_term_value = validated_data.pop('mortgage_term_value')
        mortgage_term_unit = validated_data.pop('mortgage_term_unit')

        # Calculate down_payment in dollars
        down_payment_value = decimal.Decimal(down_payment_value)
        purchase_price = decimal.Decimal(validated_data['purchase_price'])
        if down_payment_type == 'percent':
            validated_data['down_payment'] = (down_payment_value / 100) * purchase_price
        else:
            validated_data['down_payment'] = down_payment_value

        # Normalize mortgage_term to months
        if mortgage_term_unit == 'years':
            validated_data['mortgage_term'] = mortgage_term_value * 12
        else:
            validated_data['mortgage_term'] = mortgage_term_value

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'down_payment_value' in validated_data and 'down_payment_type' in validated_data:
            down_payment_value = validated_data.pop('down_payment_value')
            down_payment_type = validated_data.pop('down_payment_type')
            if down_payment_type == 'percent':
                instance.down_payment = (down_payment_value / 100) * decimal.Decimal(instance.purchase_price)
            else:
                instance.down_payment = down_payment_value

        if 'mortgage_term_value' in validated_data and 'mortgage_term_unit' in validated_data:
            mortgage_term_value = validated_data.pop('mortgage_term_value')
            mortgage_term_unit = validated_data.pop('mortgage_term_unit')
            if mortgage_term_unit == 'years':
                instance.mortgage_term = mortgage_term_value * 12
            else:
                instance.mortgage_term = mortgage_term_value

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
