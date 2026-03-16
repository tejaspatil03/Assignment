"""
Management command to seed the database with sample data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


class Command(BaseCommand):
    help = 'Seed the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        
        with transaction.atomic():
            # Create Vendors
            self.stdout.write('Creating vendors...')
            vendors = [
                Vendor(name='TechCorp Solutions', code='TECH001', description='Leading technology solutions provider'),
                Vendor(name='EduLearn Academy', code='EDU001', description='Educational content provider'),
                Vendor(name='CloudFirst Services', code='CLOUD001', description='Cloud infrastructure services'),
                Vendor(name='DataPro Systems', code='DATA001', description='Data analytics solutions'),
            ]
            for vendor in vendors:
                vendor.save()
            self.stdout.write(self.style.SUCCESS(f'Created {len(vendors)} vendors'))

            # Create Products
            self.stdout.write('Creating products...')
            products = [
                Product(name='Enterprise Software Suite', code='PROD001', description='Complete enterprise software solution'),
                Product(name='Cloud Platform', code='PROD002', description='Scalable cloud computing platform'),
                Product(name='Data Analytics Tool', code='PROD003', description='Advanced data analytics and visualization'),
                Product(name='Learning Management System', code='PROD004', description='Online learning platform'),
                Product(name='Security Suite', code='PROD005', description='Comprehensive cybersecurity solution'),
            ]
            for product in products:
                product.save()
            self.stdout.write(self.style.SUCCESS(f'Created {len(products)} products'))

            # Create Courses
            self.stdout.write('Creating courses...')
            courses = [
                Course(name='Python Programming Fundamentals', code='COURSE001', description='Learn Python from scratch'),
                Course(name='Advanced Django Development', code='COURSE002', description='Master Django framework'),
                Course(name='Cloud Architecture Basics', code='COURSE003', description='Introduction to cloud architecture'),
                Course(name='Data Science with Python', code='COURSE004', description='Data science and machine learning'),
                Course(name='Cybersecurity Essentials', code='COURSE005', description='Fundamentals of cybersecurity'),
                Course(name='DevOps Practices', code='COURSE006', description='Modern DevOps methodologies'),
            ]
            for course in courses:
                course.save()
            self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))

            # Create Certifications
            self.stdout.write('Creating certifications...')
            certifications = [
                Certification(name='Python Developer Certificate', code='CERT001', description='Certified Python developer'),
                Certification(name='Django Expert Certification', code='CERT002', description='Advanced Django certification'),
                Certification(name='AWS Cloud Practitioner', code='CERT003', description='AWS cloud fundamentals'),
                Certification(name='Data Scientist Professional', code='CERT004', description='Professional data scientist'),
                Certification(name='Security+ Certified', code='CERT005', description='Cybersecurity certification'),
            ]
            for cert in certifications:
                cert.save()
            self.stdout.write(self.style.SUCCESS(f'Created {len(certifications)} certifications'))

            # Create Vendor-Product Mappings
            self.stdout.write('Creating vendor-product mappings...')
            vendor_product_mappings = [
                VendorProductMapping(vendor=vendors[0], product=products[0], primary_mapping=True),
                VendorProductMapping(vendor=vendors[0], product=products[1], primary_mapping=False),
                VendorProductMapping(vendor=vendors[1], product=products[3], primary_mapping=True),
                VendorProductMapping(vendor=vendors[2], product=products[1], primary_mapping=True),
                VendorProductMapping(vendor=vendors[2], product=products[2], primary_mapping=False),
                VendorProductMapping(vendor=vendors[3], product=products[2], primary_mapping=True),
                VendorProductMapping(vendor=vendors[3], product=products[4], primary_mapping=False),
            ]
            for mapping in vendor_product_mappings:
                mapping.save()
            self.stdout.write(self.style.SUCCESS(f'Created {len(vendor_product_mappings)} vendor-product mappings'))

            # Create Product-Course Mappings
            self.stdout.write('Creating product-course mappings...')
            product_course_mappings = [
                ProductCourseMapping(product=products[0], course=courses[0], primary_mapping=True),
                ProductCourseMapping(product=products[0], course=courses[1], primary_mapping=False),
                ProductCourseMapping(product=products[1], course=courses[2], primary_mapping=True),
                ProductCourseMapping(product=products[1], course=courses[5], primary_mapping=False),
                ProductCourseMapping(product=products[2], course=courses[3], primary_mapping=True),
                ProductCourseMapping(product=products[3], course=courses[0], primary_mapping=True),
                ProductCourseMapping(product=products[4], course=courses[4], primary_mapping=True),
            ]
            for mapping in product_course_mappings:
                mapping.save()
            self.stdout.write(self.style.SUCCESS(f'Created {len(product_course_mappings)} product-course mappings'))

            # Create Course-Certification Mappings
            self.stdout.write('Creating course-certification mappings...')
            course_certification_mappings = [
                CourseCertificationMapping(course=courses[0], certification=certifications[0], primary_mapping=True),
                CourseCertificationMapping(course=courses[1], certification=certifications[1], primary_mapping=True),
                CourseCertificationMapping(course=courses[2], certification=certifications[2], primary_mapping=True),
                CourseCertificationMapping(course=courses[3], certification=certifications[3], primary_mapping=True),
                CourseCertificationMapping(course=courses[4], certification=certifications[4], primary_mapping=True),
                CourseCertificationMapping(course=courses[5], certification=certifications[2], primary_mapping=False),
            ]
            for mapping in course_certification_mappings:
                mapping.save()
            self.stdout.write(self.style.SUCCESS(f'Created {len(course_certification_mappings)} course-certification mappings'))

        self.stdout.write(self.style.SUCCESS('\n✓ Database seeding completed successfully!'))
        self.stdout.write('\nSample data created:')
        self.stdout.write(f'  - {Vendor.objects.count()} vendors')
        self.stdout.write(f'  - {Product.objects.count()} products')
        self.stdout.write(f'  - {Course.objects.count()} courses')
        self.stdout.write(f'  - {Certification.objects.count()} certifications')
        self.stdout.write(f'  - {VendorProductMapping.objects.count()} vendor-product mappings')
        self.stdout.write(f'  - {ProductCourseMapping.objects.count()} product-course mappings')
        self.stdout.write(f'  - {CourseCertificationMapping.objects.count()} course-certification mappings')
