window.onload = function () {

    $('.basket_list').on('click', 'input[type="number"]', function () {
        let t_href = event.target;
        // console.log(t_href.name, t_href.value);

        $.ajax(
            {
                url: "/basketapp/edit/" + t_href.name + "/" + t_href.value,
                success: function (data) {
                    // console.log(data)
                    $('.basket_list').html(data.result);
                }
            }
        )
    })

    $('.btn-outline-success').on('click',
        function (event) {
            let produt_id = event.target.value
            // console.log(produt_id);
            $

            $.ajax(
                {
                    url: "/basketapp/add/" + produt_id,
                    success: function (data) {
                        $('.card_add_basket').html(data.result)
                    }
                }
            )
        })

    let quantity, price, orderitem_num, delta_quantity, order_quantity, delta_cost;
    let quantity_array = [];
    let price_array = [];
    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text().replace(',', '.')) || 0;
    let order_total_cost = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i = 0; i < total_forms; i++) {
        quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val())
        price = parseInt($('.orderitems-' + i + '-price').text().replace(',', '.'))

        quantity_array[i] = quantity;
        if (price) {
            price_array[i] = price
        } else {
            price_array[i] = 0;
        }

    }
    // console.info('QUANTITY_ARRAY', quantity_array)
    // console.info('PRICE_ARRAY', price_array)

    //1 METOD
    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''))
        if (price_array[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_array[orderitem_num]
            quantity_array[orderitem_num] = orderitem_quantity
            orderSummaryUpdate(price_array[orderitem_num], delta_quantity)
        }


    })


    // 2 METOD
    // $('.order_form').on('click', 'input[type=checkbox]', function () {
    //     let target = event.target;
    //     console.log(target)
    //     orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''))
    //     if (target.checked) {
    //         delta_quantity = -quantity_array[orderitem_num]
    //
    //     } else {
    //         delta_quantity = quantity_array[orderitem_num]
    //
    //     }
    //     orderSummaryUpdate(price_array[orderitem_num], delta_quantity)

    // })

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2))
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_cost.toString() + ',00');
    }


    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    })


    function deleteOrderItem(row) {
        console.log(row[0].querySelector('input[type="number"]').name)
        let target_name = row[0].querySelector('input[type="number"]').name
        console.log('target name: ', target_name)
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''))
        delta_quantity = -quantity_array[orderitem_num]
        orderSummaryUpdate(price_array[orderitem_num], delta_quantity)
    }

    $(document).on('change', '.order_form select', function () {
        // $('.order_form select').change(function () {

        let target = event.target
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        // console.log(target)
        let orderitem_product_pk = target.options[target.selectedIndex].value;

        if (orderitem_product_pk) {
            $.ajax({
                url: '/ordersapp/product/' + orderitem_product_pk + '/price/',
                success: function (data) {
                    let price_html = '<span class="orderitems-' + orderitem_num + '-price">'
                        + data.price.toString().replace('.', ',') + '</span> руб';

                    let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                    current_tr.find('td:eq(2)').html(price_html)
                }
            })
        }


    })

    $(document).on('change', '.order_form select', function () {

        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        let orderitem_product_pk = target.options[target.selectedIndex].value;

        console.log(orderitem_num)
        console.log(orderitem_product_pk)

        if (orderitem_product_pk) {
            $.ajax({
                url: '/ordersapp/product/' + orderitem_product_pk + '/price/',
                success: function (data) {
                    if (data.price) {
                        price_array[orderitem_num] = parseFloat(data.price)
                        if (isNaN(quantity_array[orderitem_num])) {
                            quantity_array[orderitem_num] = 0;
                        }
                        let price_html = '<span class="orderitems-' + orderitem_num + '-price">'
                            + data.price.toString().replace('.', ',') + '</span> руб';
                        let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        current_tr.find('td:eq(2)').html(price_html)
                    }
                }
            })
        }
    })
}