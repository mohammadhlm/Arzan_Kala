$(".payment_option input").change(function () {
    let form_data = new FormData()
    form_data.append("csrfmiddlewaretoken",$('#Completion_User__Information input[name="csrfmiddlewaretoken"]').val())
    form_data.append("first_name",$("#id_first_name").val())
    form_data.append("last_name",$("#id_last_name").val())
    form_data.append("select_city",$("#id_select_city").val())
    form_data.append("location_first",$("#id_location_first").val())
    form_data.append("postal_code",$("#id_postal_code").val())
    form_data.append("phone_number",$("#id_phone_number").val())
    form_data.append("select_post_method",$(this).val())

    if ($(this).prop("checked") === true){
        $.ajax({
            url:location.href,
            type:"POST",
            data:form_data,
            processData:false,
            contentType:false,
            success:function (Response) {
                if(Response.status_code === 200){
                    $("#total_pr_price").text(Response.Calc_Postage["Total_Cost_Show"])
                    $("#Postal_Cost").text(Response.Calc_Postage["Postal_Cost"])
                }
            }
        })
    }
})