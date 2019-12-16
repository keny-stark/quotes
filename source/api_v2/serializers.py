from rest_framework import serializers
from webapp.models import Quote


class QuotesSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'text', 'created_at', 'status',
                  'author_name', 'author_email', 'rating']
