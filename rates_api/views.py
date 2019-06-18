import decimal
import logging
import requests

from django.conf import settings
from django.db.models import Q, Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Price, Port
from .serializers import AveragePriceSerializer, UploadPriceSerializer, UploadPriceUSDSerializer

logger = logging.getLogger(__name__)


class AveragePriceView(APIView):

    def get(self, request, format=None):
        serializer = AveragePriceSerializer(data=request.GET)
        if serializer.is_valid():
            origin = Port.objects.filter(Q(region__slug__iexact=serializer.validated_data['origin']) | Q(code__iexact=serializer.validated_data['origin']))
            dest = Port.objects.filter(Q(region__slug__iexact=serializer.validated_data['destination']) | Q(code__iexact=serializer.validated_data['destination']))
            prices = Price.objects.filter(
                origin__in=origin,
                destination__in=dest,
                day__range=[serializer.validated_data['date_from'], serializer.validated_data['date_to']]
            ).values('day').annotate(
                average_price=Avg('price')
            )
            return Response(prices)
        else:
            return Response(serializer.errors)


class AveragePriceWithNullView(APIView):

    def get(self, request, format=None):
        serializer = AveragePriceSerializer(data=request.GET)
        if serializer.is_valid():
            origin = Port.objects.filter(Q(region__slug__iexact=serializer.validated_data['origin']) | Q(code__iexact=serializer.validated_data['origin']))
            dest = Port.objects.filter(Q(region__slug__iexact=serializer.validated_data['destination']) | Q(code__iexact=serializer.validated_data['destination']))
            prices = Price.objects.filter(
                origin__in=origin,
                destination__in=dest,
                day__range=[serializer.validated_data['date_from'], serializer.validated_data['date_to']]
            ).values('day').annotate(
                average_price=Avg('price'), prices_count=Count('price')
            )
            prices_with_null = []
            for item in prices:
                prices_with_null.append({
                    'day': item['day'],
                    'average_price': None if item['prices_count'] < 3 else item['average_price']
                })
            return Response(prices_with_null)
        else:
            return Response(serializer.errors)


class UploadPriceView(APIView):

    def post(self, request, format=None):
        serializer = UploadPriceSerializer(data=request.POST)
        if serializer.is_valid():
            try:
                serializer.save()
                data = {
                    'success': True,
                    'message': 'Records updated successfully.'
                }
            except Exception as ex:
                logger.error(ex)
                data = {
                    'success': False,
                    'message': 'Internal server error'
                }
            return Response(data)
        else:
            return Response(serializer.errors)


class UploadPriceUSDView(APIView):

    def post(self, request, format=None):
        serializer = UploadPriceUSDSerializer(data=request.POST)
        if serializer.is_valid():
            try:
                currency = serializer.validated_data['currency']
                oer_api_url = 'https://openexchangerates.org/api/latest.json'
                oer_api_url += '?app_id={}&symbols={}'.format(settings.OER_APP_ID, currency)
                api_response = requests.get(oer_api_url, timeout=30)
                api_response = api_response.json()
                exchange_rate = api_response['rates'].get(currency)
                if exchange_rate:
                    post_data = request.POST.copy()
                    post_data['price'] = round(float(serializer.validated_data['price']) / exchange_rate, 2)
                    post_data['price'] = decimal.Decimal(str(post_data['price']))
                    serializer2 = UploadPriceUSDSerializer(data=post_data)
                    serializer2.is_valid()
                    serializer2.save()
                    data = {
                        'success': True,
                        'message': 'Records updated successfully.'
                    }
                else:
                    data = {
                        'success': False,
                        'message': 'Could not perform the currency conversion.'
                    }
            except Exception as ex:
                logger.error(ex)
                data = {
                    'success': False,
                    'message': 'Internal server error'
                }
            return Response(data)
        else:
            return Response(serializer.errors)
