//Get User Information Form
$(window).load(() => {
    $.ajax({
        url: location.origin + "/user/change_user_information/",
        type: "GET",
        success: function (form) {
            $("#change-user-information-section").html(form)
        }
    })
})


$("#change-user-information-section").on("click", '#user-profile-box', function () {
    $(this).parents("#change-user-information-section").find('input[name="user_profile"]').click()
})

//Send User Information Form
$("#change-user-information-section").on("click", "#user-information-form button", function () {
    let form_data = new FormData()
    form_data.append("user_profile", $(this).parents("#user-information-form").first().find('input[name="user_profile"]')[0].files[0])
    form_data.append('csrfmiddlewaretoken', $(this).parents("#user-information-form").first().find('input[name="csrfmiddlewaretoken"]').val())
    form_data.append('first_name', $(this).parents("#user-information-form").first().find('input[name="first_name"]').val())
    form_data.append('last_name', $(this).parents("#user-information-form").first().find('input[name="last_name"]').val())
    form_data.append('gender_selection', $(this).parents("#user-information-form").first().find('select[name="gender_selection"]').val())
    form_data.append('postal_code', $(this).parents("#user-information-form").first().find('input[name="postal_code"]').val())
    form_data.append('phone_number', $(this).parents("#user-information-form").first().find('input[name="phone_number"]').val())
    form_data.append('location_first', $(this).parents("#user-information-form").first().find('textarea[name="location_first"]').val())
    $.ajax({
        url: location.origin + "/user/change_user_information/",
        type: "POST",
        data: form_data,
        contentType: false,
        processData: false,
        success: function (Response) {
            if(Response.status === 200){
                    toastr.success(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                })
            }else{
                  toastr.error("لطفا مقادیر فیلد هارا چک کنید و به راهنمای آن ها توجه کنید...", {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                })
            }
        }
    })
})