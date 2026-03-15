from django.db import models
from core.base_model import TimeStampedModel
from product.models import Product
from course.models import Course


class ProductCourseMapping(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productcoursemapping')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='productcoursemapping')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product} → {self.course} (primary={self.primary_mapping})"
