from django.urls import path

from core.inventory.views.material.views import *
from core.inventory.views.stock.views import *
from core.inventory.views.entry.views import *
from core.inventory.views.output.views import *
from core.inventory.views.movements.views import *

urlpatterns = [
    # Material
    path('material/', MaterialListView.as_view(), name='material_list'),
    path('material/add/', MaterialCreateView.as_view(), name='create_material'),
    path('material/update/<int:pk>', MaterialUpdateView.as_view(), name='update_material'),
    path('material/delete/<int:pk>', MaterialDeleteView.as_view(), name='delete_material'),
    # Stock
    path('stock/', StockListView.as_view(), name='stock_list'),
    # Entry
    path('entry/', EntryListView.as_view(), name='entry_list'),
    path('entry/add/', EntryCreateView.as_view(), name='create_entry'),
    path('entry/delete/<int:pk>', EntryDeleteView.as_view(), name='delete_entry'),
    # Output
    path('output/', OutputListView.as_view(), name='output_list'),
    path('output/add/', OutputCreateView.as_view(), name='create_output'),
    path('output/delete/<int:pk>', OutputDeleteView.as_view(), name='delete_output'),
    # Movements
    path('movements/', MaterialMovements.as_view(), name='material_movements'),
]
