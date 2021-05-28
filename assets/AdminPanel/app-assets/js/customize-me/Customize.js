//Customizer
$('button#save_changes_customizer_form').click(()=>{
    Send__Form__Customize()
})

function Send__Form__Customize() {
    let form_data = new FormData()
    //CSRF
    form_data.append('csrfmiddlewaretoken', $('#customizer__form input[name="csrfmiddlewaretoken"]').val())
    //GET COLOR Menu
    let list_menu_color = $('ul#list__customize__menu__color li.color-box.selected').attr('class').split(' ')
    const menu__color = list_menu_color.filter(function (value, index, arr) {
        return value.length === 2
    })
    form_data.append('menu_color', menu__color)
    //GET THEME Color
    form_data.append('theme_color', $('#customize__theme__color input:checked').attr('value'))
    //Get Menu Mode
    form_data.append('menu_mode', $('#customize__menu__mode input').prop('checked'))
    //GET HEADER COLOR
    const list_header_color = $('#customize__header__color li.color-box.selected').attr('class').split(' ')
    const header_color = list_header_color.filter(function (value, index, arr) {
        return value.length === 2
    })
    form_data.append('header_color', header_color)
    //GET HEADER MODE
    form_data.append('header_mode', $('#customize__header__mode input:checked').prop('value'))
    //GET FOOTER MODE
    form_data.append('footer_mode', $('#customize__footer__mode input:checked').prop('value'))
    //GET NAVIGATION MODE
    form_data.append('flash_navigation_mode', $('#customize__navigation__mode input').prop("checked"))

    $.ajax({
        url: location.origin + '/manager/customize/',
        type: 'POST',
        contentType: false,
        processData: false,
        data: form_data,
        success: function (Msg) {
            if (Response.status ===200){
                toastr.success(Response.messages, {
                    tapToDismiss: false,
                    positionClass: "toast-top-center",
                    progressBar: true,
                });
            }
        }

    })
}

//Change Color Menu
$(document).ready(() => {
    //Menu Color
    $('#list__customize__menu__color .color-box.selected').click()
    //Theme Color
    $('div#customize__theme__color input:checked').click()
    //Menu MODE
    $('#customize__menu__mode input.selected').click()
    //Header Color
    $('#customize__header__color li.selected').click()
    //Header Mode
    $('#customize__header__mode input:checked').click()
    //FOOTER MODE
    $('#customize__footer__mode input:checked').click()
    //NAVIGATION MODE
    $('#customize__navigation__mode input.selected').click()
})
