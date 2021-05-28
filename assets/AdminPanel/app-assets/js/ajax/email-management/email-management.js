/*
In this function, the ID sends the clicked email to View
 and displays the content of the received email in a template.
*/
$('#email-content li.media').click(function () {
    let Email_id = $(this).attr("id").split("-")[1]
    $.ajax({
        url: location.href,
        type: "GET",
        data: {
            email_id: Email_id
        },
        success: function (Mail_Msg) {
            $('#mail-msg-content').html(Mail_Msg)
        }
    })
})

/*
* Receive Email Delete Form This form is received at the same time as loading the page
* And is added to the page
*/
$(document).ready(() => {
    $.ajax({
        url: location.origin + "/manager/removed-mail",
        type: "GET",
        success: function (html_form) {
            $("#removed-mail-form-section").html(html_form)
        }
    })
})

/*
* This function is used to send an email delete request. It is called at the same time
*  as pressing the trash can icon and adds the emails in a string ID and
*  sends the request to the view.
* */
$("#removed__mail-btn").click(function () {
    let id_str = ''
    $.each($("li.media input:checked"), function (index, val) {
        if (index === 0) {
            id_str += $(this).val()
        } else {
            id_str += "," + $(this).val()
        }
    })
    let form_data = new FormData()
    form_data.append("removed_mail_id", id_str)
    form_data.append("csrfmiddlewaretoken", $('#removed-mail-form input[name="csrfmiddlewaretoken"]').val())
    $.ajax({
        url: location.origin + "/manager/removed-mail/",
        type: "POST",
        data: form_data,
        contentType: false,
        processData: false,
        success: function (Response) {
            if (Response.status === 200){
                toastr.success(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }else if(Response.status === 203){
                toastr.warning(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
})