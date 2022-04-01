import json
from django.core.management.base import BaseCommand

from authapp.models import User
from mainapp.models import ProductCategory, Product


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:

        return json.load(infile)


def reinit_categories(fixture_path):
    categories = load_from_json(fixture_path)

    ProductCategory.objects.all().delete()
    for category in categories:
        cat = category.get('fields')
        cat['id'] = category.get('pk')
        new_category = ProductCategory(**cat)
        new_category.save()


def reinit_products(fixture_path):
    products = load_from_json(fixture_path)

    Product.objects.all().delete()
    for product in products:
        prod = product.get('fields')
        category = prod.get('category')
        _category = ProductCategory.objects.get(id=category)
        prod['category'] = _category
        new_category = Product(**prod)
        new_category.save()


def create_admin(login, password, email):
    User.objects.create_superuser(
        username=login, email=email, password=password)


class Command(BaseCommand):
    def handle(self, operation, *args, **options):
        pass
        print(f"{operation}")
        create_admin("admin", "1", "admin@test.ru")
        reinit_categories('mainapp/fixtures/category.json')
        reinit_products('mainapp/fixtures/products.json')
