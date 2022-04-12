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
            console.log(produt_id);
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
}