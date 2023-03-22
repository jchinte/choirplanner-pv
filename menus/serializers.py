from .models import MenuItem
import rest_framework.serializers as serializers

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'link_page', 'link_url', 'open_in_new_tab', 'page', 'sort_order', 'title', 'slug']