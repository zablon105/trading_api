from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Trade
from .serializers import TradeSerializer


class TradeListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/trades/        → list all trades
    POST /api/trades/        → create a new trade (MQL5 bot posts here)
    """
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [AllowAny]  # will add auth later


class TradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/trades/<id>/  → get single trade
    PUT    /api/trades/<id>/  → update trade
    DELETE /api/trades/<id>/  → delete trade
    """
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
def trade_summary(request):
    """
    GET /api/trades/summary/
    Returns overall trading statistics
    """
    trades = Trade.objects.all()
    total_trades    = trades.count()
    open_trades     = trades.filter(status='OPEN').count()
    closed_trades   = trades.filter(status='CLOSED').count()
    total_profit    = sum(t.profit for t in trades if t.profit is not None)
    winning_trades  = trades.filter(profit__gt=0).count()
    losing_trades   = trades.filter(profit__lt=0).count()

    return Response({
        'total_trades'  : total_trades,
        'open_trades'   : open_trades,
        'closed_trades' : closed_trades,
        'total_profit'  : round(total_profit, 2),
        'winning_trades': winning_trades,
        'losing_trades' : losing_trades,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def close_trade(request, pk):
    """
    POST /api/trades/<id>/close/
    Marks a trade as closed with final price and profit
    """
    try:
        trade = Trade.objects.get(pk=pk)
    except Trade.DoesNotExist:
        return Response(
            {'error': 'Trade not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if trade.status == 'CLOSED':
        return Response(
            {'error': 'Trade is already closed'},
            status=status.HTTP_400_BAD_REQUEST
        )

    trade.status      = 'CLOSED'
    trade.close_price = request.data.get('close_price', trade.close_price)
    trade.profit      = request.data.get('profit', trade.profit)
    trade.close_time  = timezone.now()
    trade.save()

    return Response(TradeSerializer(trade).data)