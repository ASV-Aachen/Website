from .models import profile
import django_filters

class userFilter(django_filters.FilterSet):
    class Meta:
        model = profile
        fields = ['status']
    

