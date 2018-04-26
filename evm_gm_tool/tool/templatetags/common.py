from django import template
from ..models import *
# from django.contrib.staticfiles.templatetags.staticfiles import static
from django.templatetags.static import static
from django.conf import settings
register = template.Library()

SERVER_BASE_URL = 'http://{}:{}/'.format(settings.SERVER_IP, settings.SERVER_PORT)
@register.filter
def get_avatar_url(user):
    return Utils.get_avatar_url(user)

@register.filter
def get_avatar_url_by_user_id(user_id):
    return Utils.get_avatar_url_by_user_id(user_id)
