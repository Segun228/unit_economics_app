from rest_framework import serializers
from .models import ModelSet, UnitModel


class UnitModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitModel
        fields = [
            'id',
            'user',
            'model_set',
            'users',
            'customers',
            'AVP',
            'APC',
            'TMS',
            'COGS',
            'COGS1s',
            'created_at',
            'updated_at',
            'FC'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ModelSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSet
        fields = [
            'id',
            'user',
            'name',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ModelSetReadSerializer(serializers.ModelSerializer):

    units = UnitModelSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ModelSet
        fields = [
            'id',
            'user',
            'name',
            'description',
            'created_at',
            'updated_at',
            'units',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

