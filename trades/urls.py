from django.urls import path
from . import views

urlpatterns = [
    path('trades/',                               views.TradeListCreateView.as_view(), name='trade-list-create'),
    path('trades/summary/',                       views.trade_summary,                 name='trade-summary'),
    path('trades/analytics/',                     views.trade_analytics,               name='trade-analytics'),
    path('trades/by-ticket/<int:ticket>/',        views.trade_by_ticket,               name='trade-by-ticket'),
    path('trades/by-ticket/<int:ticket>/update/', views.update_trade_by_ticket,        name='trade-update-by-ticket'),
    path('trades/<int:pk>/',                      views.TradeDetailView.as_view(),     name='trade-detail'),
    path('trades/<int:pk>/close/',                views.close_trade,                   name='trade-close'),
    path('account/',                              views.get_account_snapshot,          name='account-get'),
    path('account/update/',                       views.update_account_snapshot,       name='account-update'),
    path('health/',                               views.health_check,                  name='health-check'),
]