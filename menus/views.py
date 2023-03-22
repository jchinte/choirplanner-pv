from django.http import Http404
from django.shortcuts import render
import rest_framework.generics as generics
from .serializers import MenuSerializer
from .models import Menu
# Create your views here.

class MenuListView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        if 'slug' in self.request.query_params:
            try:
                return Menu.objects.get(slug=self.request.query_params['slug']).menu_items
            except Menu.DoesNotExist:
                raise Http404
        try:
            return Menu.objects.first().menu_items
        except Menu.DoesNotExist:
            raise Http404
