from django.db import models
from core.base_model import TimeStampedModel
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='coursecertificationmapping')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE,
                                      related_name='coursecertificationmapping')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('course', 'certification')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.course} → {self.certification} (primary={self.primary_mapping})"
