from django.db import models

class BorrowerAssessment(models.Model):
    # Input Data
    age = models.IntegerField()
    income = models.FloatField()
    loan_amount = models.FloatField()
    loan_tenure_months = models.IntegerField()
    loan_purpose = models.CharField(max_length=50)
    loan_type = models.CharField(max_length=50)
    residence_type = models.CharField(max_length=50)
    
    # Credit History
    avg_dpd_per_dm = models.IntegerField(default=0)
    total_loan_months = models.IntegerField(default=0)
    credit_utilization_ratio = models.FloatField(default=0)
    dmtlm = models.FloatField(default=0)
    
    # Results
    default_probability = models.FloatField()
    credit_score = models.IntegerField()
    rating = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment {self.id} - Score: {self.credit_score} ({self.rating})"
