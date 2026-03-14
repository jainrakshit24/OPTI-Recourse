from django.urls import path
from .views import PredictCreditRiskView, AssessmentHistoryView, BulkPredictView, AnalyticsView

urlpatterns = [
    path('predict/', PredictCreditRiskView.as_view(), name='predict-risk'),
    path('bulk-predict/', BulkPredictView.as_view(), name='bulk-predict'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('history/', AssessmentHistoryView.as_view(), name='assessment-history'),
]
