//---- User Edit -----//
/*Sending default user model information as Ajax*/
$('button#btn-apply-changes').click(function () {
    let form_data = new FormData()
    $.each($('form#form_default_user input'), function (index, value) {
        form_data.append($(value).attr("name"), $(value).val())
    })
    $.each($('div.custom-checkbox input[type="checkbox"]'), function (index, value) {
        if ($(value).attr('type') === 'checkbox') {
            form_data.append($(value).attr("name"), $(value).prop("checked"))
        }
    })
    $.ajax({
        url: location.href,
        data: form_data,
        type: 'POST',
        processData: false,
        contentType: false,
        success: function (Response) {
            if (Response.bool === true) {
                toastr.success(Response.text, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            } else {
                toastr.warning(Response.text, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
})

//----User Information
/*Receive profile models that have a one-to-one relationship with the user model*/
$(document).ready(function () {
    const user_id = location.pathname.split("edit-user/")[1]
    $.ajax({
        url: location.origin + "/manager/user/save-information/" + user_id,
        type: "GET",
        success: function (Form) {
            $("div#div-form-user-info").html(Form)
            $('button#btn-apply-changes').click(send_form_user_info)
            $('input#id_user_profile').change(prev_img_user_profile)
        }
    })
})

/*Send profile model information that is one-to-one with the user model*/
function send_form_user_info() {
    let form_data_user_info = new FormData()
    const user_id = location.pathname.split("edit-user/")[1]
    $.each($('form#form_information_user input'), function (index, value) {
        if ($(value).attr("type") === "checkbox") {
            form_data_user_info.append($(value).attr("name"), $(value).prop("checked"));
        } else if ($(value).attr("type") === "file") {
            if ($(value)[0].files.length === 1) {
                form_data_user_info.append($(value).attr("name"), $(value)[0].files[0])
            }
        } else if ($(value).attr("type") === "text") {
            form_data_user_info.append($(value).attr("name"), $(value).val());
        } else if ($(value).attr("type") === "number") {
            form_data_user_info.append($(value).attr("name"), $(value).val());
        } else if ($(value).attr("type") === "hidden") {
            form_data_user_info.append($(value).attr("name"), $(value).val());
        }
    })
    $.each($('form#form_information_user select'), function (index, value) {
        form_data_user_info.append($(value).attr("name"), $(value).val());
    })
    $.each($('form#form_information_user textarea'), function (index, value) {
        form_data_user_info.append($(value).attr("name"), $(value).val());
    })
    $.ajax({
        url: location.origin + "/manager/user/save-information/" + user_id,
        type: 'POST',
        data: form_data_user_info,
        contentType: false,
        processData: false,
        success: function (Response) {
            if (Response.bool === true) {
                toastr.success(Response.text, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            } else {
                toastr.warning(Response.text, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
}


// --User Profile
/*This function is to check the deletion of the user profile
Click the Delete Profile button to check the function of the delete photo box
Then, after deleting the photo, the tick removes it*/
$('button#user-photo-delete-btn').click(() => {
    let form_delete_photo = new FormData()
    const ch_bx_delete_photo = $('input[name="delete_profile_checkbox"]')
    ch_bx_delete_photo.prop("checked", true)
    form_delete_photo.append($(ch_bx_delete_photo).attr("name"), $(ch_bx_delete_photo).prop("checked"))
    form_delete_photo.append("csrfmiddlewaretoken", $('form#form_information_user input[name="csrfmiddlewaretoken"]').val())
    const user_id = location.pathname.split("edit-user/")[1]
    $.ajax({
        url: location.origin + "/manager/user/save-information/" + user_id,
        type: 'POST',
        data: form_delete_photo,
        contentType: false,
        processData: false,
        success: (Response) => {
            ch_bx_delete_photo.prop("checked", false)
            if (Response.bool === true) {
                $('img#preview-user-profile').prop("src", location.origin + Response.src)
                toastr.success(Response.text, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            } else {
                 $('img#preview-user-profile').prop("src", location.origin + Response.src)
                toastr.warning(Response.text, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
})
// Change User Photo
$('button#user-photo-change-btn').click(() => {
    $('input#id_user_profile').click()
})

function prev_img_user_profile() {
    const file = $('input[name="user_profile"]')[0].files[0]
    if (file) {
        let reader = new FileReader()
        reader.onload = () => {
            $('img#preview-user-profile').prop('src', reader.result);
        }
        reader.readAsDataURL(file);
    }
}
