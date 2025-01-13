from django.db import models

class TestCase(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    explanation = models.TextField(blank=True, null=True)
    sample_test_case = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Input: {self.input}, Output: {self.output}"
