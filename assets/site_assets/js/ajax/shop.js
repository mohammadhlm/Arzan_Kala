$(document).ready(() => {
    $.ajax({
        url: location.origin + "/ajax-filter/",
        type: "GET",
        success: function (data) {
            $("#product-section").append(data)
        }
    })
})


$('div.main_content').on("click", "button#get_new_product", function () {
    let container = $(this).parents(".container")
    let brand_list_id = []
    let category_list_id = []
    $.each($(container).find(".widget_categories .form-check-input"), function () {
        if ($(this).prop("checked") === true) {
            category_list_id.push($(this).prop("id").split("_")[1])
        }
    })
    $.each($(container).find(".list_brand .form-check-input"), function () {
        if ($(this).prop("checked") === true) {
            brand_list_id.push($(this).prop("id").split("_")[1])
        }
    })
    $.ajax({
        url:location.origin+"/ajax-filter/",
        type:"GET",
        data:{
            order:$(container).find('select#id_order').val(),
            price_filter:`${$(container).find("#price_first").val()}-${$(container).find("#price_second").val()}`,
            category_id:category_list_id.toString(),
            brand_id:brand_list_id.toString()
        },

        success:function (data) {
            $("#product-section").find(".shop_container").remove()
            $("#product-section").append(data)
        }
    })

})
