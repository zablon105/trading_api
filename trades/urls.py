from django.urls import path
from . import views

urlpatterns = [
    path('trades/',           views.TradeListCreateView.as_view(), name='trade-list-create'),
    path('trades/summary/',   views.trade_summary,                 name='trade-summary'),
    path('trades/<int:pk>/',  views.TradeDetailView.as_view(),     name='trade-detail'),
    path('trades/<int:pk>/close/', views.close_trade,             name='trade-close'),
    path('health/', views.health_check, name='health-check'),
]