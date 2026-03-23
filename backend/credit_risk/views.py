import sys
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import Avg, Count
import pandas as pd

# Add parent directory to sys.path to import utils from the original project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils import predict, bulk_predict

from .models import BorrowerAssessment
from .serializers import BorrowerAssessmentSerializer

class PredictCreditRiskView(APIView):
    def post(self, request):
        serializer = BorrowerAssessmentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Use the existing logic in utils.py
            results = predict(**data)
            
            # Save the assessment to history
            assessment = BorrowerAssessment.objects.create(
                **data,
                default_probability=results['probability'],
                credit_score=results['credit_score'],
                rating=results['rating']
            )
            
            results['id'] = assessment.id
            return Response(results, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BulkPredictView(APIView):
    def post(self, request):
        if not isinstance(request.data, list):
            return Response({"error": "Expected a list of borrower profiles"}, status=status.HTTP_400_BAD_REQUEST)
        
        df = pd.DataFrame(request.data)
        results = bulk_predict(df)
        
        # Save all assessments in bulk
        assessments = []
        for i, item in enumerate(request.data):
            assessments.append(BorrowerAssessment(
                **item,
                default_probability=results[i]['probability'],
                credit_score=results[i]['credit_score'],
                rating=results[i]['rating']
            ))
        
        BorrowerAssessment.objects.bulk_create(assessments)
        return Response(results, status=status.HTTP_201_CREATED)

class AnalyticsView(APIView):
    def get(self, request):
        # Summary statistics
        summary = BorrowerAssessment.objects.aggregate(
            avg_score=Avg('credit_score'),
            total_count=Count('id'),
            avg_income=Avg('income'),
            avg_loan=Avg('loan_amount')
        )
        
        # Rating distribution
        dist = BorrowerAssessment.objects.values('rating').annotate(count=Count('id'))
        
        # Purpose distribution
        purpose_dist = BorrowerAssessment.objects.values('loan_purpose').annotate(
            count=Count('id'),
            avg_score=Avg('credit_score')
        )
        
        # Timeline (last 30 days)
        timeline = BorrowerAssessment.objects.extra(select={'day': 'date(created_at)'}).values('day').annotate(count=Count('id')).order_by('day')
        
        # Scatter data for income vs score
        scatter = BorrowerAssessment.objects.values('income', 'credit_score', 'rating')[:500]
        
        return Response({
            "summary": summary,
            "rating_distribution": list(dist),
            "purpose_distribution": list(purpose_dist),
            "timeline": list(timeline),
            "scatter_data": list(scatter)
        })

class AssessmentHistoryView(generics.ListAPIView):
    queryset = BorrowerAssessment.objects.all().order_by('-created_at')
    serializer_class = BorrowerAssessmentSerializer
