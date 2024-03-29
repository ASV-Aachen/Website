# yourapp/lookups.py
from ajax_select import register, LookupChannel
from .models import *
from django.db.models import Q
from django.core.exceptions import PermissionDenied

@register('responsible')
class responsibleLookup(LookupChannel):

    model = User 

    def get_query(self, q, request):
        # print("TEST")
        return self.model.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q)).order_by('last_name')[:20]

    def format_item_display(self, item):
        return u"<span class='tag'>%s %s</span>" % (item.first_name, item.last_name)
    
    def check_auth(self, request):
        if request.user.is_authenticated:
            return True
        raise PermissionDenied
        return False

@register('employee')
class employeeLookup(LookupChannel):

    model = account

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:20]
    
    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name

    def check_auth(self, request):
        if request.user.is_authenticated:
            return True
        raise PermissionDenied
        return False

@register('tags')
class TagsLookup(LookupChannel):

    model = tag

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name

    def check_auth(self, request):
        if request.user.is_authenticated:
            return True
        raise PermissionDenied
        return False
