from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
        # product = Product.objects.filter(
        #     Q(category__name='Обувь') | Q(id=5)
        # )
        #
        # product = Product.objects.filter(
        #     Q(category__name='Обувь') & Q(id=5)
        # )
        # product = Product.objects.filter(
        #     ~Q(category__name='Обувь')
        # )
        # product = Product.objects.filter(
        #     Q(category__name='Обувь'), id=5
        # )
        # print(product)
