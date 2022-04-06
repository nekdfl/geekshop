import json
from django.core.management.base import BaseCommand

from authapp.models import User
from mainapp.models import ProductCategory, Product


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:
        return json.load(infile)


def load_category_fixture():
    categories = load_from_json('mainapp/fixtures/dump_category.json')

    ProductCategory.objects.all().delete()
    for category in categories:
        cat = category.get('fields')
        cat['id'] = category.get('pk')
        new_category = ProductCategory(**cat)
        new_category.save()

def load_product_fixture():
    products = load_from_json('mainapp/fixtures/dump_product.json')
    Product.objects.all().delete()
    for product in products:
        prod = product.get('fields')
        category = prod.get('category')
        _category = ProductCategory.objects.get(id=category)
        prod['category'] =_category
        new_category = Product(**prod)
        new_category.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser(username='gns', email='admin@mail.ru', password='1')
        load_category_fixture()
        load_product_fixture()


