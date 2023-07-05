import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def release_date_validator(date):
    if date > datetime.datetime.today():
        raise ValidationError(
            _("%(date)s shouldn't be more than now"), params={"date": date}
        )
