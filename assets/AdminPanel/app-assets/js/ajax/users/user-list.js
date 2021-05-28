//---- User List -----//
//Get & Add Form Default User And User Info Form
//Fetch Form Default User
async function get_default_user_form() {
    return await fetch(location.origin + "/manager/user/default-user-form/", {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        method: "GET",
    })
}

$('#add-a-user-medal').on('shown.bs.modal', () => {
    get_default_user_form()
        .then((default_user_form) => {
            if (default_user_form.status === 200) {
                return default_user_form.text()
            }else{
                toastr.warning('متاسفانه نتواسنتیم فرم ثبت کاربر را از سرور دریافت کنیم.', 'اخطار!', {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });

            }
        })
        .then((default_user_form) => {
            /*In this section, the received default user form is added to the page*/
            $('div#modal-body_add_user').html(default_user_form)
        }).then(() => {
        $('button#Send__default__user__form').click(() => {
            /*In this part, the main user form of the information is sent to View to register*/
            let form_data = new FormData()
            $.each($('form#default__user_form input'), function (index, val) {
                if ($(this).attr("type") === "checkbox") {
                    form_data.append($(this).attr("name"), $(this).prop("checked"))
                } else if ($(this).attr("type") !== "checkbox" && $(this).attr("name") !== "username") {
                    form_data.append($(this).attr("name"), $(this).val())
                } else if ($(this).attr("type") !== "checkbox" && $(this).attr("name") === "username") {
                    let email_dt = $('form#default__user_form input[name="email"]').val()
                    form_data.append($(this).attr("name"), email_dt)
                }
            })
            send_default_user_form(form_data)
        })
    })
})

//Send Form Default User
function send_default_user_form(default__user_form) {
    $.ajax({
        type: "POST",
        url: location.origin + "/manager/user/default-user-form/",
        data: default__user_form,
        contentType: false,
        processData: false,
        success: function (Msg) {
            if (Msg.created === true) {
                get_user_info_form(Msg.pk)
            }
        }
    })
}


//Fetch Form User Info
async function get_user_info_form(pk) {
    return await fetch(location.origin + "/manager/user/user-info-form/" + pk, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        method: "GET",
    }).then(user_info_form => {
        if (user_info_form.status === 200) {
            return user_info_form.text()
        }
    }).then(user_info_form => {
        $('div#modal-body_add_user').html(user_info_form)
        $('div#user-photo-upload-box').click(() => {
            $('input[name="user_profile"]').click()
        })
        $('input[name="user_profile"]').change(function () {
            let file = $(this)[0].files[0]
            if (file) {
                let reader = new FileReader();
                reader.onload = function () {
                    $('div#user-photo-upload-box').removeClass('d-flex').addClass('d-none')
                    $('img#preview-user-profile').prop('src', reader.result).removeClass('d-none').addClass('d-block')
                }
                reader.readAsDataURL(file);
            }
        })
    }).then(() => {
        $('button#Send__user__info__form').click(() => {
            let form_data = new FormData()
            $.each($('form#user__information_form input'), function (index, val) {
                if ($(this).attr("type") !== 'files') {
                    form_data.append($(this).attr('name'), $(this).val())
                } else if ($(this).attr("type") === 'files') {
                    form_data.append($(this).attr('name'), $(this)[0].files)
                }
            })
            $.each($('form#user__information_form select'), function (index, val) {
                form_data.append($(this).attr('name'), $(this).val())
            })
            $.each($('form#user__information_form textarea'), function (index, val) {
                form_data.append($(this).attr('name'), $(this).val())
            })
            send_user__information_form(form_data, pk)
        })
    })
}


//Send User Info Update Form
function send_user__information_form(form_data, pk) {
    $.ajax({
        url: location.origin + "/manager/user/user-info-form/" + pk,
        data: form_data,
        type: 'POST',
        contentType: false,
        processData: false,
        success: function (Response) {
            if (Response.created === true) {
                $('span#close_modal_register_user').parent('button').click()
                 toastr.success(Response.msg_text, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
}


//Delete User
$(document).ready(function () {
    $.ajax({
        url: location.origin + "/manager/user/delete-user/",
        type: "GET",
        success: function (delete_user_form) {
            $('p.d-btn').append(delete_user_form)

        }
    })
})
$('button#del-user-btn').click(() => {
    swal({
        title: "آیا اطمینان دارید؟",
        text: "با تایید کردن این گزینه تمامی کاربران انتخاب شده و اطلاعات آنها بطور کامل حذف خواهد شد!",
        icon: "warning",
        className: 'text-right',
        buttons: ["انصراف", "تایید"],
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                let all_del_user = []
                let form_data=new FormData()
                $.each($("div.selector_for__jq input:checked"), function () {
                    all_del_user.push($(this).attr('id').split("-")[1])
                })
                form_data.append('csrfmiddlewaretoken',$('form#delete_user_form input[name="csrfmiddlewaretoken"]').val())
                form_data.append('user_id',all_del_user)
                $.ajax({
                    url:location.origin+'/manager/user/delete-user/',
                    type:'POST',
                    data:form_data,
                    contentType:false,
                    processData:false,
                    success:function (Msg){
                        if(Msg.status===200){
                            console.log(Msg.status)
                            swal("تمام کاربران انتخاب شده با موفقیت حذف شدند.", {
                                icon: "success",
                                timer: 2000,
                                button: "خروج",
                            });
                        }
                    }
                })
            } else {
                swal("شما از حذف کاربران صرف نظر کردبد!", {
                    icon: 'warning',
                    timer: 2000,
                    button: "خروج",
                });
            }
        });
})
//User Advanced Filter
$('#div_advanced__user__filter .form-group select').change(function () {
    let user_role = null, user_status = null, user_gender = null;
    if ($('#users-list-role').val() === 'all_permissions') {
        user_role = 'null'
    } else if ($('#users-list-role').val() === 'is_superuser') {
        user_role = true
    } else if ($('#users-list-role').val() === 'is_member') {
        user_role = false
    }

    if ($('#users-list-status').val() === 'all_status') {
        user_status = 'null'
    } else if ($('#users-list-status').val() === 'true') {
        user_status = true
    } else if ($('#users-list-status').val() === 'false') {
        user_status = false
    }

    if ($('#users-list-gender').val() === 'all_gender') {
        user_gender = 'null'
    } else if ($('#users-list-gender').val() === 'MR') {
        user_gender = "MR"
    } else if ($('#users-list-gender').val() === 'MS') {
        user_gender = "MS"
    } else if ($('#users-list-gender').val() === 'TG') {
        user_gender = "TG"
    }
    $.ajax({
        url: location.origin + "/manager/user/advanced-user-filter/",
        type: 'GET',
        data: {
            role: user_role,
            status: user_status,
            gender: user_gender
        },
        success: function (Content) {
            $('#content_user_list').html(Content)
        }
    })
})