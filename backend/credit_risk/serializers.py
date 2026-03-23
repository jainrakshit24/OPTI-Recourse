from rest_framework import serializers
from .models import BorrowerAssessment

class BorrowerAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowerAssessment
        fields = '__all__'
        read_only_fields = ('default_probability', 'credit_score', 'rating', 'created_at')
