"""
Seed management command.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Vendors
        v1, _ = Vendor.objects.get_or_create(code='VND001', defaults={'name': 'Vendor Alpha', 'description': 'First vendor'})
        v2, _ = Vendor.objects.get_or_create(code='VND002', defaults={'name': 'Vendor Beta', 'description': 'Second vendor'})

        # Products
        p1, _ = Product.objects.get_or_create(code='PRD001', defaults={'name': 'Product One', 'description': 'First product'})
        p2, _ = Product.objects.get_or_create(code='PRD002', defaults={'name': 'Product Two', 'description': 'Second product'})

        # Courses
        c1, _ = Course.objects.get_or_create(code='CRS001', defaults={'name': 'Course Alpha', 'description': 'Intro course'})
        c2, _ = Course.objects.get_or_create(code='CRS002', defaults={'name': 'Course Beta', 'description': 'Advanced course'})

        # Certifications
        cert1, _ = Certification.objects.get_or_create(code='CERT001', defaults={'name': 'Cert Gold', 'description': 'Gold certification'})
        cert2, _ = Certification.objects.get_or_create(code='CERT002', defaults={'name': 'Cert Silver', 'description': 'Silver certification'})

        # Mappings
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p1, defaults={'primary_mapping': True})
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p2, defaults={'primary_mapping': False})
        VendorProductMapping.objects.get_or_create(vendor=v2, product=p2, defaults={'primary_mapping': True})

        ProductCourseMapping.objects.get_or_create(product=p1, course=c1, defaults={'primary_mapping': True})
        ProductCourseMapping.objects.get_or_create(product=p2, course=c2, defaults={'primary_mapping': True})

        CourseCertificationMapping.objects.get_or_create(course=c1, certification=cert1, defaults={'primary_mapping': True})
        CourseCertificationMapping.objects.get_or_create(course=c2, certification=cert2, defaults={'primary_mapping': True})

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
