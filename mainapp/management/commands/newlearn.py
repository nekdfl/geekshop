from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q, F, When, Case, IntegerField

from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_3 = 3

        action_1_time_delta = timedelta(hours=12)
        action_2_time_delta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_condition = Q(order__updated__lte=F('order_created') + action_1_time_delta)

        action_2_condition = Q(order__updated__gt=F('order_created') + action_1_time_delta +
                                                  Q(order_updated_lte=F('order_created') + action_2_time_delta))
        action_3_condition = Q(order__updated__gt=F('order_created') + action_2_time_delta)

        action_1_order = When(action_1_condition, then=ACTION_1)
        action_2_order = When(action_2_condition, then=ACTION_2)
        action_3_order = When(action_3_condition, then=ACTION_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * -action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        test_data = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField()
            )
        )
        # .annotate(total_proce=Case(
        #     action_1_price,
        #     action_2_price,
        #     action_3_price,
        #     output_field=DecimalField())
        # ).order_by('action_order', 'total_proce').select_related()

        # t_list = PrettyTable(['Заказ', 'Товар', 'Скидка', 'Разнрица времени', ])
        # t_list.align = "1"
        i = 0
        # for orderitem in test_data:
        #     t_list.add_
