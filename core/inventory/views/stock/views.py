import json

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from core.security.mixins import PermissionMixin
from core.inventory.forms import Inventory, StockForm


class StockListView(PermissionMixin, ListView):
    model = Inventory
    template_name = 'stock/list.html'
    permission_required = 'view_inventory'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Stock de materiales'
        return context












