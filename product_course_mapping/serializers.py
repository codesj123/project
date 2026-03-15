from rest_framework import serializers
from .models import ProductCourseMapping


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCourseMapping
        fields = [
            'id', 'product', 'course', 'primary_mapping',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        product = data.get('product', getattr(self.instance, 'product', None))
        course = data.get('course', getattr(self.instance, 'course', None))
        primary_mapping = data.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))

        # Duplicate mapping check
        qs = ProductCourseMapping.objects.filter(product=product, course=course)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A mapping between this product and course already exists."
            )

        # Single primary mapping per product
        if primary_mapping:
            primary_qs = ProductCourseMapping.objects.filter(
                product=product, primary_mapping=True, is_active=True
            )
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This product already has a primary course mapping."
                )

        return data
