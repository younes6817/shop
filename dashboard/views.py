from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from app_order.models import *
from app_product.models import *
from app_user.models import *
from django.db.models import Sum
from django.utils.timezone import now
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from datetime import timedelta, date
import jdatetime

PERSIAN_MONTHS = [
    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
]
PERSIAN_DAYS = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']

@staff_member_required
def home(request):
    current_month = now().month
    current_year = now().year
    today = now().date()
    today_shamsi = jdatetime.date.today()

    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.filter(role="customer").count()
    total_sales = Order.objects.filter(status="paid").aggregate(
        total=Sum('total_price')
    )['total'] or 0
    monthly_sales = Order.objects.filter(
        status='paid',
        created_at__year=current_year,
        created_at__month=current_month
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    yearly_sales = Order.objects.filter(
        status='paid',
        created_at__year=current_year
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # weekly data
    weekday = today_shamsi.weekday()
    saturday = today_shamsi - timedelta(days=weekday)

    week_dates_shamsi = []
    week_labels = []
    week_data = []

    for i in range(7):
        day_shamsi = saturday + timedelta(days=i)
        day_gregorian = day_shamsi.togregorian()
        
        total = Order.objects.filter(
            status='paid',
            created_at__date=day_gregorian
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        week_dates_shamsi.append(day_shamsi)
        # برچسب: "۲۳ فروردین" یا "شنبه ۲۳"
        label = f"{day_shamsi.day} {PERSIAN_MONTHS[day_shamsi.month-1]}"
        week_labels.append(label)
        week_data.append(total)

    # monthly data
    first_day = today_shamsi.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(day=29)
        next_month = first_day + timedelta(days=32)
        last_day = next_month.replace(day=1) - timedelta(days=1)
    else:
        next_month = first_day.replace(month=first_day.month+1, day=1)
        last_day = next_month - timedelta(days=1)

    month_labels = []
    month_data = []
    current = first_day
    while current <= last_day:
        gregorian = current.togregorian()
        total = Order.objects.filter(
            status='paid',
            created_at__date=gregorian
        ).aggregate(total=Sum('total_price'))['total'] or 0
        month_labels.append(current.strftime("%d"))
        month_data.append(total)
        current += timedelta(days=1)

    # yearly data
    year_labels = []
    year_data = []

    for m in range(1, 13):
        start_shamsi = jdatetime.date(today_shamsi.year, m, 1)
        
        if m == 12:
            end_shamsi = jdatetime.date(today_shamsi.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_shamsi = jdatetime.date(today_shamsi.year, m + 1, 1) - timedelta(days=1)
        
        total = Order.objects.filter(
            status='paid',
            created_at__date__gte=start_shamsi.togregorian(),
            created_at__date__lte=end_shamsi.togregorian()
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        year_labels.append(PERSIAN_MONTHS[m-1])
        year_data.append(total)

    print("Week data:", week_data)
    print("Month data:", month_data)
    print("Year data:", year_data)



    return render(request, 'home_panel.html', {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
        'total_sales': total_sales,
        "monthly_sales": monthly_sales,
        "yearly_sales": yearly_sales,
        'week_labels': week_labels,
        'week_data': week_data,
        'monthly_labels': month_labels,
        'monthly_data': month_data,
        'yearly_labels': year_labels,
        'yearly_data': year_data,
    })