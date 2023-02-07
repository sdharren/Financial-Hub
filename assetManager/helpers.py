from django.utils import timezone

def make_aware_date(naive_date):
    return timezone.make_aware(naive_date, timezone.get_default_timezone())