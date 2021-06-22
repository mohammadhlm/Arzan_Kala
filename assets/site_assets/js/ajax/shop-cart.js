//Get Form Remove Cart Item In List
$(window).load(function () {
    $.ajax({
        url: location.origin + "/remove-product-from-cart",
        type: "GET",
        success: function (Data) {
            $("#remove-product-section").html(Data)
        }
    })
})

$('.add-to-cart-icon').click(function () {
    delete_or_add_product_ajax($(this).attr("id").split("_")[1])
})
//Remove Cart Item In List
$("#cart-item-list_drop__down").on("click", "a.item_remove", function () {
    delete_or_add_product_ajax($(this).find("i").attr("id").split("_")[1])
})

//Add Cart Item In List Product Detail
$("#btn-addtocart_Product_Detail").on("click", function () {
    delete_or_add_product_ajax($(this).find("i").attr("id").split("_")[1])
})

//Delete Or Add Product To Cart
function delete_or_add_product_ajax(product_id) {
    let form_data = new FormData()
    form_data.append('csrfmiddlewaretoken', $('#delete_add-product-from-cart input[name="csrfmiddlewaretoken"]').val())
    form_data.append('product_id', product_id)
    $.ajax({
        url: location.origin + "/remove-product-from-cart",
        type: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (Response) {
            if (Response.status === 800) {
                let isnum = /^\d+$/.test($('#cart-item-count').html());
                if (isnum) {
                    let product__counter = parseInt($('#cart-item-count').html());
                    product__counter += 1;
                    $('#cart-item-count').html(product__counter);
                }
                let cart_item = `<li id="item_${Response.product_id}">
                                            <a href="#" class="item_remove"><i class="ion-close" id="product_${Response.product_id}"></i></a>
                                            <a href="${Response.get_absolute_url}"><img src="${location.origin + Response.item_product_photo_url}" alt="cart_thumb1">
                                                ${Response.product_name}
                                            </a>
                                            <span class="cart_quantity"> ${Response.item_count} عدد ${Response.item_total} <span class="cart_amount"> <span
                                                    class="price_symbole">تومان</span></span></span>
                                        </li>`
                $('#cart-item-list_drop__down').append(cart_item)

                $("#product_total_price").html(Response.total_product_price)
                $('.amount').html(Response.total_product_price)
                toastr.success(Response.msg, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                })
            } else if (Response.status === 700) {
                $('li#item_' + Response.delete_product_id).remove()
                let isnum = /^\d+$/.test($('#cart-item-count').html());
                if (isnum) {
                    let product__counter = parseInt($('#cart-item-count').html());
                    product__counter -= 1;
                    $('#cart-item-count').html(product__counter);
                    $("#product_total_price").html(Response.total_product_price)
                    $('.amount').html(Response.total_product_price)
                    toastr.warning(Response.msg, {
                        tapToDismiss: false,
                        positionClass: "toast-top-center",
                        progressBar: true,
                    })
                }
            }else if(Response.status === 900){
                 toastr.warning(Response.msg, {
                        tapToDismiss: false,
                        positionClass: "toast-top-center",
                        progressBar: true,
                    })
            }
        }
    })
}