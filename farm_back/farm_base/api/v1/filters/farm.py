from django_filters import FilterSet

from farm_base.models import Farm


class FarmFilter(FilterSet):

    class Meta:
        model = Farm
        fields = ['id', 'state', 'municipality', 'name', 'owner__name', 'owner__document', 'owner__document_type']
