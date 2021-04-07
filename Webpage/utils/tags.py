from django import template

from web.models import frontHeader

'''
Check for Template
@example: {% if request.user|has_group:"Editor" %}
'''
register = template.Library()

@register.filter('has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.simple_tag
def getLeftFront():
    return frontHeader.objects.all()[0].left

@register.simple_tag
def getRightFront():
    return frontHeader.objects.all()[0].right
