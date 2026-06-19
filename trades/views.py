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


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    GET /api/health/
    Returns a simple production health status.
    """
    return Response({'status': 'ok', 'environment': 'production'})

@api_view(['GET'])
@permission_classes([AllowAny])
def trade_analytics(request):
    """
    GET /api/trades/analytics/
    Returns detailed analytics: equity curve, win rate, profit by symbol, etc.
    """
    trades = Trade.objects.filter(status='CLOSED').order_by('open_time')

    # Equity curve - cumulative profit over time
    equity_curve = []
    cumulative = 0
    for t in trades:
        if t.profit is not None:
            cumulative += float(t.profit)
            equity_curve.append({
                'date': t.close_time.strftime('%Y-%m-%d %H:%M') if t.close_time else t.open_time.strftime('%Y-%m-%d %H:%M'),
                'cumulative_profit': round(cumulative, 2),
                'trade_profit': float(t.profit),
                'ticket': t.ticket,
            })

    # Profit by symbol
    symbols = {}
    for t in trades:
        if t.profit is not None:
            symbols.setdefault(t.symbol, 0)
            symbols[t.symbol] += float(t.profit)
    profit_by_symbol = [{'symbol': k, 'profit': round(v, 2)} for k, v in symbols.items()]

    # Win/loss stats
    wins = [float(t.profit) for t in trades if t.profit and t.profit > 0]
    losses = [float(t.profit) for t in trades if t.profit and t.profit < 0]
    total_closed = trades.count()
    win_rate = round((len(wins) / total_closed * 100), 1) if total_closed > 0 else 0
    avg_win = round(sum(wins) / len(wins), 2) if wins else 0
    avg_loss = round(sum(losses) / len(losses), 2) if losses else 0
    profit_factor = round(abs(sum(wins) / sum(losses)), 2) if losses and sum(losses) != 0 else 0

    # Max drawdown (simplified - biggest peak-to-trough drop in equity curve)
    max_drawdown = 0
    peak = 0
    running = 0
    for t in trades:
        if t.profit is not None:
            running += float(t.profit)
            if running > peak:
                peak = running
            drawdown = peak - running
            if drawdown > max_drawdown:
                max_drawdown = drawdown

    # Daily P&L (last 30 days)
    from django.db.models.functions import TruncDate
    from django.db.models import Sum
    daily = (
        trades.exclude(close_time__isnull=True)
        .annotate(day=TruncDate('close_time'))
        .values('day')
        .annotate(total=Sum('profit'))
        .order_by('day')
    )
    daily_pnl = [{'date': str(d['day']), 'profit': float(d['total'] or 0)} for d in daily]

    return Response({
        'equity_curve': equity_curve,
        'profit_by_symbol': profit_by_symbol,
        'daily_pnl': daily_pnl,
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_factor': profit_factor,
        'max_drawdown': round(max_drawdown, 2),
        'total_wins': len(wins),
        'total_losses': len(losses),
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def trade_by_ticket(request, ticket):
    """
    GET /api/trades/by-ticket/<ticket>/
    Look up a trade's Django ID and current data by its MT5 ticket number.
    Used by the EA to find which record to update/close.
    """
    try:
        trade = Trade.objects.get(ticket=ticket)
    except Trade.DoesNotExist:
        return Response(
            {'error': 'Trade not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(TradeSerializer(trade).data)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_trade_by_ticket(request, ticket):
    """
    PATCH /api/trades/by-ticket/<ticket>/update/
    Partial update (e.g. SL/TP change) for an open trade, matched by MT5 ticket.
    """
    try:
        trade = Trade.objects.get(ticket=ticket)
    except Trade.DoesNotExist:
        return Response(
            {'error': 'Trade not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TradeSerializer(trade, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)