import random
import qrcode
from django.db.models import F
from api.email import email
from api.models import RetailObject, Employee
from settings.celery import app


@app.task
def updating_debt_task():
    queryset = RetailObject.objects.all()
    debt = random.randint(5, 500)
    queryset.update(debt=(F("debt") + debt))
    return True


@app.task
def reduce_debt_task():
    queryset = RetailObject.objects.all()
    debt = random.randint(100, 10000)
    for new_debt in queryset:
        if new_debt.debt <= 0:
            queryset.update(debt=0)
        else:
            queryset.update(debt=(F("debt") - debt))
    return True


@app.task
def reset_debt_task(queryset):
    return queryset.update(debt=0)


@app.task
def send_email_task(data, employee_id):
    qr_code = qrcode.make(data)
    qr_code.save("api/static/qr_code.png")
    employee_email = Employee.objects.get(id=employee_id).email
    email(employee_email)
