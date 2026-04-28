def is_payment_successful(code):
    return code == 100


def get_callback_url():
    return "http://127.0.0.1:8000/payment/verify/"