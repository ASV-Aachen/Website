# yourapp/lookups.py
from ajax_select import register, LookupChannel
from .models import *
from django.db.models import Q
from django.core.exceptions import PermissionDenied

@register('sailors')
class sailorsLookup(LookupChannel):

    model = sailor

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('name')[:20]
    
    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name

    def check_auth(self, request):
        if request.user.is_authenticated:
            return True
        raise PermissionDenied
        return False