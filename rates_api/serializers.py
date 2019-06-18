from datetime import timedelta
from rest_framework import serializers
from rest_framework.fields import empty

from .models import Port, Price


class AveragePriceSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    origin = serializers.CharField(max_length=75)
    destination = serializers.CharField(max_length=75)

    def validate(self, attrs):
        # check if date_from is greater than date_to
        if attrs['date_from'] > attrs['date_to']:
            raise serializers.ValidationError("date_from must be less than or equal to date_to")
        return attrs



class UploadPriceSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    origin = serializers.CharField(max_length=5)
    destination = serializers.CharField(max_length=5)
    price = serializers.DecimalField(decimal_places=2, max_digits=20)

    def validate(self, attrs):
        # check if date_from is greater than date_to
        if attrs['date_from'] > attrs['date_to']:
            raise serializers.ValidationError("date_from must be less than or equal to date_to")
        # check if the given origin port code exists
        if not Port.objects.filter(code__iexact=attrs['origin']).exists():
            raise serializers.ValidationError({'origin': 'The given port code is invalid.'})
        # check if the given destination port code exists
        if not Port.objects.filter(code__iexact=attrs['destination']).exists():
            raise serializers.ValidationError({'destination': 'The given port code is invalid.'})
        return attrs

    def save(self, **kwargs):
        price_objs = []
        date = self.validated_data['date_from']
        origin = Port.objects.get(code__iexact=self.validated_data['origin'])
        dest = Port.objects.get(code__iexact=self.validated_data['destination'])
        while date <= self.validated_data['date_to']:
            price_objs.append(
                Price(origin=origin, destination=dest, day=date, price=self.validated_data['price'])
            )
            date += timedelta(days=1)
        if price_objs:
            Price.objects.bulk_create(price_objs)


class UploadPriceUSDSerializer(UploadPriceSerializer):
    currency = serializers.CharField(max_length=3)
