# app_product/templatetags/persian_numbers.py
from django import template

register = template.Library()

@register.filter
def to_persian_number(value):
    """تبدیل اعداد انگلیسی به فارسی"""
    if value is None:
        return ''
    
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'  # ← دقت کن: ۲ و ۵ و ۸ هم باشه!
    english_digits = '0123456789'
    
    result = ''
    for char in str(value):
        if char in english_digits:
            result += persian_digits[english_digits.index(char)]
        else:
            result += char
    
    return result

@register.filter
def to_persian_price(value):
    """تبدیل قیمت به فرمت فارسی با جداکننده هزارگان"""
    if value is None:
        return '0'
    
    try:
        num = int(float(value))
    except (ValueError, TypeError):
        return str(value)
    
    # اضافه کردن جداکننده هزارگان
    num_str = '{:,}'.format(num)
    
    # تبدیل به فارسی
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    result = ''
    for char in num_str:
        if char in english_digits:
            result += persian_digits[english_digits.index(char)]
        else:
            result += char
    
    return result