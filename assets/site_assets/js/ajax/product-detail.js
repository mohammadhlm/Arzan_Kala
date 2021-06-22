$(document).ready(() => {
    let slug = $("div#comment-sections").attr("name")
    if (slug !== undefined) {
        $.ajax({
            url: location.origin + "/send-comment/" + slug,
            type: "GET",
            success: function (data) {
                $("#comment-sections").html(data)
            }
        })
    }
})

$(".main_content").on("click", "button#send-comment-btn", function () {
    let form_data = new FormData();
    let form_element = $(this).parents("form#send-comment")
    form_data.append("csrfmiddlewaretoken", $(this).parents("form#send-comment").find('input[name="csrfmiddlewaretoken"]').val())
    form_data.append("body", $(this).parents("form#send-comment").find('input[name="body"]').val())
    form_data.append("user", $(this).parents("form#send-comment").find('input[name="user"]').val())
    form_data.append("product", $(this).parents("form#send-comment").find('input[name="product"]').val())
    let slug = $("div#comment-sections").attr("name")
    $.ajax({
        url: location.origin + "/send-comment/" + slug,
        type: "POST",
        data: form_data,
        contentType: false,
        processData: false,
        success: function (data) {
            if (data.status !== undefined) {
                $(form_element).remove()
            }
        }
    })
})

//Get Rating Form
$(document).ready(() => {
    let slug = $("div#rating-section").attr("name")
    if (slug !== undefined) {
        $.ajax({
            url: location.origin + "/send-rating/" + slug,
            type: "GET",
            success: function (data) {
                $("#rating-section").html(data)
            }
        })
    }
})

$(".main_content").on("click", ".star_rating span", function () {
    if (!$(this).hasClass("selected")) {
        $(this).addClass("selected").prevAll().addClass("selected")
    } else {
        $(this).parent().find("span.selected").last().removeClass("selected").prevAll().removeClass("selected")
    }
})

$('.main_content').on("click", "button#send-rating-form", function () {
    if (slug !== undefined) {
        let form_data = new FormData()
        form_data.append("star", $(this).parents("form#rating-form").first().find("span.selected").last().attr("data-value"))
        form_data.append("csrfmiddlewaretoken", $(this).parents("form#rating-form").first().find('input[name="csrfmiddlewaretoken"]').first().val())
        form_data.append("product", $(this).parents("form#rating-form").first().find('select#id_product').first().val())
        form_data.append("user", $(this).parents("form#rating-form").first().find('input#id_user').first().val())
        let slug = $("div#rating-section").attr("name")
        $.ajax({
            url: location.origin + "/send-rating/" + slug,
            type: "POST",
            data: form_data,
            contentType: false,
            processData: false,
            success: function (data) {
                $("#rating-section").html(data)
            }
        })
    }
})

