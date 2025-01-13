from django.db import models

class TestCase(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.input} -> {self.output}"
