from rest_framework import serializers
from app_admin.models import Country, Region, Zone, Woreda
from conceptnote.models import *


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('__all__')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('__all__')

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('__all__')

class WoredaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Woreda
        fields = ('__all__')

class IcnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icn
        fields = ('__all__')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('__all__')