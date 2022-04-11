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


    $('#add_to_cart').on('click', function () {
        let t_href = event.target.value;
        console.log(t_href);

        // $.ajax(
        //     {
        //         url:"/basketapp/edit/" + t_href.name + "/" + t_href.value,
        //         success: function (data){
        //             // console.log(data)
        //             $('.basket_list').html(data.result);
        //         }
        //     }
        // )
    })
}