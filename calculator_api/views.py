from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import CalculatorInputSerializer
from .constants import INSTRUMENTS, CHOICES
from .utils import CalculatorContext, calculate_lot_risk


class CalculateView(APIView):
    def post(self, request: Request) -> Response:
        serializer = CalculatorInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            context = CalculatorContext(
                account_balance=data['account_balance'],
                entry_price=data['entry_price'],
                stop_price=data['stop_price'],
                risk_percent=data['risk_percent'],
                lowest_allowable_lot=data['lowest_lot']
            )

            lot, pips, total_risk = calculate_lot_risk(context)

            return Response({
                'lot': float(lot),
                'pips': float(pips),
                'risk': float(total_risk),
                'lowest_lot': float(context.lowest_allowable_lot)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstrumentListView(APIView):
    def get(self, request: Request) -> Response:
        data = [
            {"code": code, "name": name, "min_lot": INSTRUMENTS.get(code)}
            for code, name in CHOICES
        ]

        return Response(data, status=status.HTTP_200_OK)
