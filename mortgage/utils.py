import time
import requests
from django.conf import settings
import logging

logger = logging.getLogger('mortgage')


def get_mortgage_payments(loan_amount, interest_rate, term_in_months, retries=3, timeout=10):
    """
    Fetch mortgage payment details from API Ninjas.

    Args:
        loan_amount (Decimal): The total loan amount.
        interest_rate (Decimal): The annual interest rate in percent.
        term_in_months (int): The term of the loan in months.
        retries (int): Number of retry attempts for the API call.
        timeout (int): Timeout in seconds for the API call.

    Returns:
        dict: A dictionary containing 'loan_amount', 'monthly_payment', 'total_paid', 'total_interest'.

    Raises:
        Exception: If the API call fails.
    """
    api_ninjas_url = "https://api.api-ninjas.com/v1/mortgagecalculator"
    api_key = settings.API_NINJAS_KEY

    headers = {
        'X-Api-Key': api_key,
    }
    params = {
        'loan_amount': float(loan_amount),
        'interest_rate': float(interest_rate),
        'duration_years': term_in_months / 12
    }

    backoff = 2

    for attempt in range(retries):
        try:
            response = requests.get(api_ninjas_url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            logger.info(f"API Ninjas response: {data}")

            # Validate and parse required fields
            monthly_payment = data.get('monthly_payment', {}).get('mortgage')
            annual_payment = data.get('annual_payment', {}).get('mortgage')
            total_interest_paid = data.get('total_interest_paid')

            if monthly_payment is None or annual_payment is None or total_interest_paid is None:
                raise ValueError("Incomplete data received from API Ninjas.")

            return {
                'loan_amount': loan_amount,
                'monthly_payment': monthly_payment,
                'total_paid': term_in_months * monthly_payment,
                'total_interest': total_interest_paid,
            }
        except requests.RequestException as e:
            logger.error(f"Attempt {attempt + 1}: Error fetching data from API Ninjas: {e}")
            if attempt < retries - 1:
                # todo -- use a library like tenacity for more advanced retry strategies
                sleep_time = backoff ** attempt
                logger.debug(f"Retrying in {sleep_time} seconds...")
                time.sleep(timeout)
                continue
            else:
                raise Exception("Failed to fetch data from API Ninjas after multiple attempts.")
