from rest_framework import serializers
from .models import Resource, Booking
from django.contrib.auth.models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'capacity']

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)

    resource_id = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.all(), source='resource', write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'resource',
            'user',
            'resource_id',
            'start_time',
            'end_time',
            'title',
        ]

    def validate(self, data):
        instance = self.instance
        start_time = data.get('start_time', instance.start_time if instance else None)
        end_time = data.get('end_time', instance.end_time if instance else None)
        resource = data.get('resource', instance.resource if instance else None)

        if not all([start_time, end_time, resource]):
            raise serializers.ValidationError("Start time, end time and resource are required.")

        if end_time <= start_time:
            raise serializers.ValidationError("Data końcowa musi być po dacie początkowej.")

        conflicting_bookings = Booking.objects.filter(
            resource=resource,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(pk=instance.pk if instance else None)

        if conflicting_bookings.exists():
            raise serializers.ValidationError(
                f"Zasób '{resource.name}' jest już zarezerwowany w tym terminie."
            )

        return data

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user
