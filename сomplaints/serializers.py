from rest_framework import serializers
from .models import Complaint, ComplaintStatus
from users.models import CustomUser


class ComplaintStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintStatus
        fields = ['id', 'name']


class ComplaintSerializer(serializers.ModelSerializer):
    status = ComplaintStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=ComplaintStatus.objects.all(), source='status', write_only=True
    )

    class Meta:
        model = Complaint
        fields = ['id', 'sender', 'recipient', 'description', 'status', 'status_id', 'created_at']
        read_only_fields = ['id', 'created_at', 'sender', 'recipient']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Request not found in context")

        sender = request.user
        recipient = self.initial_data.get('recipient')  # recipient передаётся в "сыром" виде
        if not recipient:
            raise serializers.ValidationError({"recipient": "Это поле обязательно."})

        try:
            recipient_user = CustomUser.objects.get(id=recipient)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"recipient": "Пользователь не найден."})

        validated_data['sender'] = sender
        validated_data['recipient'] = recipient_user

        return super().create(validated_data)

