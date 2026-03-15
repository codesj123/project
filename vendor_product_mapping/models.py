from django.db import models
from core.base_model import TimeStampedModel
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendorproductmapping')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendorproductmapping')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('vendor', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor} → {self.product} (primary={self.primary_mapping})"
