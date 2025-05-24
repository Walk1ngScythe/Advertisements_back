from rest_framework import serializers
from .models import Complaint, ComplaintStatus
from app_users.models import CustomUser


class ComplaintStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintStatus
        fields = ['id', 'name']


class ComplaintSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    status = ComplaintStatusSerializer(read_only=True)
    # либо удаляешь это поле совсем, либо делаешь не обязательным
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=ComplaintStatus.objects.all(),
        source='status',
        write_only=True,
        required=False
    )
    recipient = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Complaint
        fields = ['id', 'sender', 'recipient', 'description', 'status', 'status_id', 'created_at']

