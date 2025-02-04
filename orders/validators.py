import re
from datetime import datetime

CARD_NUMBER_PATTERN = re.compile(r'^\d{4}-\d{4}-\d{4}-\d{4}$')
EXP_DATE_PATTERN = re.compile(r'^(0[1-9]|1[0-2])\/\d{4}$')
CVC_PATTERN = re.compile(r'^\d{3}$')


def validate_card_data(card_number, exp_date, cvc):
    if not CARD_NUMBER_PATTERN.match(card_number):
        return {'error': 'Invalid card number'}
    if not EXP_DATE_PATTERN.match(exp_date):
        return {'error': 'Invalid expiration date'}
    if not CVC_PATTERN.match(cvc):
        return {'error': 'Invalid CVC'}
    card_exp_date = datetime.strptime(exp_date, '%m/%Y')
    current_date = datetime.now()
    if card_exp_date < current_date:
        return {'error': 'Card expired'}
    return None
