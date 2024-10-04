from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'  # Use all fields from the model
        read_only_fields = ['user']  # Mark 'user' as read-only

    def to_internal_value(self, data):
        # Filter out any extra fields that are not part of the model
        allowed_fields = set(self.fields)  # Get all fields defined in the serializer
        filtered_data = {key: value for key, value in data.items() if key in allowed_fields}

        return super(UserSerializer, self).to_internal_value(filtered_data)
