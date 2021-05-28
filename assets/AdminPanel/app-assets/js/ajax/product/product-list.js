/*Receive an advanced product filter form.
This function is called at the same time as loading the page*/
$(document).ready(() => {
    $.ajax({
        url: location.origin + '/manager/advanced-product-filter/',
        type: 'GET',
        success: function (Form) {
            $('#div_advanced__product__filter div').append(Form)
        }
    })
})

/*Product filter form
This function inserts the result of the filtered data into the data list section*/
$('#div_advanced__product__filter').on('change', 'select#id_status', function () {
    $.ajax({
        url: location.origin + '/manager/advanced-product-filter/',
        type: 'GET',
        data: {
            status: $(this).val()
        },
        success: function (Data) {
            $('#content_product_list').html(Data)
        }
    })
})

/*This function receives the product removal form from View at the same time as loading the page
And then adds to the page*/
$(document).ready(() => {
    $.ajax({
        url: location.origin + "/manager/deleted-product/",
        type: "GET",
        success: function (deleted_product__form) {
            $("#delete_product_section").html(deleted_product__form)
        }
    })
})

/*This function is activated at the same time as pressing the delete button,
 then sends the product ID to View,
 and after processing, View sends the result to it*/
$("#del-product-btn").click(() => {
    let delete_product_id = ''
    let form_data = new FormData()
    form_data.append("csrfmiddlewaretoken", $('#deleted_product_form input[name="csrfmiddlewaretoken"]').val())
    $.each($("#selected__product").find('input[type="checkbox"]'), function (index, val) {
        if (index === 0) {
            delete_product_id += $(this).val()
        } else {
            delete_product_id += "," + $(this).val()
        }
    })
    form_data.append("deleted_product_id", delete_product_id)
    $.ajax({
        url:location.origin+"/manager/deleted-product/",
        type:"POST",
        data: form_data,
        contentType:false,
        processData:false,
        success:function (Response) {

            $('input#customCheck_'+Response.delete_product_id).parents("td").first().remove()
               if (Response.status === 200) {
                toastr.success(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            } else {
                toastr.success(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
})