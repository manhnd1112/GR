from django import template
from ..models import *
# from django.contrib.staticfiles.templatetags.staticfiles import static
from django.templatetags.static import static
register = template.Library()

SERVER_BASE_URL = 'http://127.0.0.1:8000/tool/'
@register.filter
def get_avatar_url(user):
    print(static('avatar_default.png'))
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)
    if user.userprofile.avatar and hasattr(user.userprofile.avatar, 'url'):
        return  '{}{}'.format(SERVER_BASE_URL, user.userprofile.avatar.url)
    else:
        return static('assets/avatar_default.png')