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
    month, year = map(int, exp_date.split('/'))
    if datetime(year, month, 1) < datetime.now():
        return {'error': 'Card expired'}
    return None
