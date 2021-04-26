from django import template
from users.models import User
from main.models import DoctorApplication

register = template.Library()

@register.filter(name='hasapplied')
def hasapplied(user):
    try:
        app = DoctorApplication.objects.filter(user=user).last()
    except DoctorApplication.DoesNotExist:
        app=None
    return True if app else False