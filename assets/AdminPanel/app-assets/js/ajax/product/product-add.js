/*
*This function is to select the file by clicking on the box
*/
$('#btn-add-original-product-image').click(function () {
    $('input#id_photo').click()
})
/*This function is for previewing the selected photo*/
$('input#id_photo').change(() => {
    const file = $('input[type="file"]')[0].files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function () {
            $('.prev-icon-select-photo').addClass("d-none")
            $("img#preview-product-img").attr("src", reader.result);
            $('#preview-product-img').removeClass("d-none").addClass("d-block")

        }
        reader.readAsDataURL(file);
    }
})

/*This function is to empty the photo input*/
$('#btn-del-original-product-image').click(() => {
    $('input#id_photo').val(null)
    $('.prev-icon-select-photo').removeClass("d-none")
    $('#preview-product-img').removeClass("d-block").addClass("d-none")
})

//----Modal Add Tag----
/*This function is called at the same time as the medal is opened and
receives the tag making form from View
And adds to the page
*/
$('div#new-tag-making-medal').on('shown.bs.modal', () => {
    $.ajax({
        url: location.origin + '/manager/product/create-tag/',
        type: 'GET',
        success: function (Form) {
            $('div#modal-body_add_tag').html(Form)
            $('button#btn-making-new-tag').click(() => {
                send_form_new_making_tag()
            })
        }
    })
})

/*This feature sends the new tag creation form to the view*/
function send_form_new_making_tag() {
    $.ajax({
        url: location.origin + '/manager/product/create-tag/',
        type: 'POST',
        data: $('form#form-making-new-tag').serialize(),
        success: (Response) => {
            if (Response.status === 200) {
                toastr.success(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            } else {
                toastr.warning('اطلاعات وارد شده را بررسی کنید سپس دوباره تلاش کنید.', {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        },
    })
}

//-----Modal Add Category-----
/*
*This function is called at the same time as opening the product category creation medal and
*  receives the category creation form from View
Then add it to the page
*/
$('div#new-category-making-medal').on('shown.bs.modal', () => {
    $.ajax({
        url: location.origin + '/manager/product/create-category/',
        type: 'GET',
        success: (Form) => {
            $('div#modal-body_add_category').html(Form)
            $('div#category-photo-upload-box').click(() => {
                $('input#id_category_photo').click()
            })
            $('button#btn-making-new-category').click(() => {
                send_form_making_new_category()
            })
        }
    })
})

/*
This function sends the new product category form to View
*/
function send_form_making_new_category() {
    let form_data = new FormData()
    form_data.append('category_photo', $('input[name="category_photo"]')[0].files[0])
    form_data.append('csrfmiddlewaretoken', $('form#form-making-new-category input[name="csrfmiddlewaretoken"]').val())
    form_data.append('category_name', $('form#form-making-new-category input[name="category_name"]').val())
    form_data.append('slug', $('form#form-making-new-category input[name="slug"]').val())
    $.ajax({
        url: location.origin + '/manager/product/create-category/',
        type: 'POST',
        data: form_data,
        contentType: false,
        processData: false,
        success: (Response) => {
            if (Response.status === 200) {
                toastr.success(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            } else {
                toastr.success('اطلاعات وارد شده را بررسی کنید سپس دوباره تلاش کنید.', {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
}

//-----Modal Add Brand-----
/*
This function is called at the same time as the product brand creation medal is opened
And receives the brand creation form from View and then adds it to the page
*/
$('#new-brand-making-medal').on('shown.bs.modal', function () {
    $.ajax({
        url: location.origin + '/manager/product/create-brand/',
        type: 'GET',
        success: (Form) => {
            $("#modal-body_add_brand").html(Form)
        }
    })
})

/*This function sends the new brand form to View*/
$("#modal-body_add_brand").on("click", "#btn-making-new-brand", function () {
    let form_data = new FormData()
    form_data.append("photo", $(this).parents("form").first().find('input#id_photo')[0].files[0])
    form_data.append("name", $(this).parents("form").first().find('input#id_name').val())
    form_data.append(("csrfmiddlewaretoken"), $(this).parents("form").first().find('input[name="csrfmiddlewaretoken"]').val())
    $.ajax({
        url: location.origin + "/manager/product/create-brand/",
        type: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: (Response) => {
            if (Response.status === 200) {
                toastr.success(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            } else {
                toastr.success('اطلاعات وارد شده را بررسی کنید سپس دوباره تلاش کنید.', {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
})

/*This function is called by pressing the brand image selection box
The input then calls the file selection*/
$("#modal-body_add_brand").on("click", "#brand-photo-upload-box", function () {
    $(this).parents("form").first().find('input#id_photo').click()
})


//----Modal Add Slider----
/*This function is called at the same time as the opening of the new slider construction medal
Receives the new slider build form from View
Then adds to the page*/
$('div#new-slider-making-medal').on('shown.bs.modal', () => {
    $.ajax({
        url: location.origin + '/manager/product/create-slider/',
        type: 'GET',
        success: function (Form) {
            $('div#modal-body_add_slider').html(Form)
        }
    })
})


/*This function sends the new slider build form to the view*/
$("#new-slider-making-medal").on("click", "#btn-making-new-slider", function () {
    let form_data = new FormData()
    form_data.append("text", $(this).parents("form").first().find('input#id_text').val())
    form_data.append("title", $(this).parents("form").first().find('input#id_title').val())
    form_data.append(("csrfmiddlewaretoken"), $(this).parents("form").first().find('input[name="csrfmiddlewaretoken"]').val())
    $.ajax({
        url: location.origin + "/manager/product/create-slider/",
        type: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: (Response) => {
            if (Response.status === 200) {
                toastr.success(Response.message, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            } else {
                toastr.success('اطلاعات وارد شده را بررسی کنید سپس دوباره تلاش کنید.', {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }
    })
})


/*Search tags in the database*/
$('#id_select_tag').select2({
    language: "fa",
    placeholder: 'برچسب مورد نظر خود را جستجو کنید...',
    dir: "rtl",
    ajax: {
        url: function (params) {
            return location.origin + "/manager/search-tag?text=" + params.term
        },
        dataType: 'json',
        type: "GET",
    }
});


/*Search the category in the database*/
$('#id_select_category').select2({
    language: "fa",
    placeholder: 'دسته بندی مورد نظر خود را جستجو کنید...',
    dir: "rtl",
    ajax: {
        url: function (params) {
            return location.origin + "/manager/search-category?text=" + params.term
        },
        dataType: 'json',
        type: "GET",
    }
});

/*Search a slider in the database*/
$('#id_select_slider').select2({
    language: "fa",
    placeholder: 'اسلایدر مورد نظر خود را جستجو کنید...',
    dir: "rtl",
    ajax: {
        url: function (params) {
            return location.origin + "/manager/search-live-slider?text=" + params.term
        },
        dataType: 'json',
        type: "GET",
    }
});


/*Search for a brand in a database*/
$('#id_select_brand').select2({
    language: "fa",
    placeholder: 'برند مورد نظر خود را جستجو کنید...',
    dir: "rtl",
    ajax: {
        url: function (params) {
            return location.origin + "/manager/search-live-brand?text=" + params.term
        },
        dataType: 'json',
        type: "GET",
    }
});


/*Gather information about the new product form and submit it for viewing*/
$('#create-pr-btn').click(() => {
    let attr = {}
    let color = {}
    let form_data = new FormData()
    form_data.append('csrfmiddlewaretoken', $('form#form_default_user input[name="csrfmiddlewaretoken"]').val())
    form_data.append('photo', $('form#form_default_user input[name="photo"]')[0].files[0])
    form_data.append('name', $('form#form_default_user input[name="name"]').val())
    form_data.append('status', $('form#form_default_user select[name="status"]').val())
    form_data.append('slug', $('form#form_default_user input[name="slug"]').val())
    //ADD Tag Data
    $.each($("#form_default_user #id_select_tag").val(), function (index, val) {
        form_data.append("tag", val)
    })
    //Add Cat Data
    $.each($("#form_default_user #id_select_category").val(), function (index, val) {
        form_data.append("category", val)
    })
    //Add Brand Data
    $.each($("#form_default_user #id_select_brand").val(), function (index, val) {
        form_data.append("brand", val)
    })
    //Add Slider Data
    $.each($("#form_default_user #id_select_slider").val(), function (index, val) {
        form_data.append("slider", val)
    })
    //Add Attr
    $.each($('.table-add-atr tbody tr'), function () {
        attr[$(this).children("td.dt-name").text()] = $(this).children("td.dt-name").next("td").text()
    })
    //Add Color
    $.each($('#table-body-content tr'), function () {
        color[$(this).children("td.td-color-code").text()] = $(this).children("td.td-color-code").text()
    })
    //Extra
    form_data.append("final_price", $('form#form_default_user input[name="final_price"]').val())
    form_data.append("discounted_price", $('form#form_default_user input[name="discounted_price"]').val())
    form_data.append("inventory", $('form#form_default_user input[name="inventory"]').val())
    form_data.append("sold", $('form#form_default_user input[name="sold"]').val())
    form_data.append('short_description', CKEDITOR.instances["id_short_description"].getData())
    form_data.append('further_details', CKEDITOR.instances["id_further_details"].getData())
    form_data.append('attributes', JSON.stringify(attr))
    form_data.append('color', JSON.stringify(color))
    form_data.append('publication_date', $('#inputTextDate1').val().split(" ")[1].split("/").join("-") + " " + $('#inputTextDate1').val().split(" ")[0])
    $.ajax({
        url: location.origin + "/manager/product/create-product/",
        data: form_data,
        type: "POST",
        contentType: false,
        processData: false,
        success: function (Data) {
            if (Data.status !== undefined && Data.status === 200) {
                toastr.info('این محصول با موفقیت ساخته شد در مرحله بعد شما باید تصاویر بیشتر برای محصول خود انتخاب کنید', 'محصول ایجاد شد', {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
            if (Data.status === undefined) {
                if (Data.category !== undefined) {
                    $('p#err_pr_category').removeClass("d-none").text(Data.category)
                } else {
                    $('p#err_pr_category').addClass("d-none")
                }

                if (Data.final_price !== undefined) {
                    $('p#err_pr_final_price').removeClass("d-none").text(Data.final_price)
                } else {
                    $('p#err_pr_final_price').addClass("d-none")
                }

                if (Data.further_details !== undefined) {
                    $('p#err-pr-further_details').removeClass("d-none").text(Data.further_details)
                } else {
                    $('p#err-pr-further_details').addClass("d-none")
                }

                if (Data.inventory !== undefined) {
                    $('p#err_pr_inventory').removeClass("d-none").text(Data.inventory)
                } else {
                    $('p#err_pr_inventory').addClass("d-none")
                }

                if (Data.name !== undefined) {
                    $('p#err_pr_name').removeClass("d-none").text(Data.name)
                } else {
                    $('p#err_pr_name').addClass("d-none")
                }

                if (Data.photo !== undefined) {
                    $('p#err_pr_photo').removeClass("d-none").text(Data.photo)
                } else {
                    $('p#err_pr_photo').addClass("d-none")
                }

                if (Data.short_description !== undefined) {
                    $('p#err-pr-short_description').removeClass("d-none").text(Data.short_description)
                } else {
                    $('p#err-pr-short_description').addClass("d-none")
                }

                if (Data.tag !== undefined) {
                    $('p#err_pr_tag').removeClass("d-none").text(Data.tag)
                } else {
                    $('p#err_pr_tag').addClass("d-none")
                }
            }
        }
    })
})

/*Date and time selection module to Tehran time*/
$('#inputTextDate1').MdPersianDateTimePicker({
    selectedDate: new Date(),
    targetTextSelector: '#inputTextDate1',
    targetDateSelector: '#inputTextDate1',
    placement: "bottom",
    dateFormat: "yyyy-MM-dd HH:mm:ss",
    englishNumber: true,
});
function calendarViewOnChange() {
    let New_Time = ""
    New_Time += $('#inputTextDate1').val().split(" ")[1]
    New_Time += " " + $('#inputTextDate1').MdPersianDateTimePicker('getText');
    $('#inputTextDate1').val(New_Time)
}
