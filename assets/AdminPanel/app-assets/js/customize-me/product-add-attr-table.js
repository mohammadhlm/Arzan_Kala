$('button#add-attr-btn').click(function(){
    $("#add-attr-sidebar").children("div.overlay-bg").toggleClass("show")
    $("#add-attr-sidebar").children('div.add-new-data').toggleClass("show")
})

//
$('button#add-atr-btn-form').click(()=>{
    let data_name =[]
    $.each($('td.dt-name'),function (index,value) {
        data_name.push($(value).text())
    })
    const gen_random_number=()=>{
        let id_tr = ""
        for (let i = 0; i < 5; i++) {
            id_tr+=String.fromCharCode(Math.floor(Math.random()*(90-65)+65))
        }
        return id_tr+Math.floor(Math.random()*100)
    }
    if ($('input#data-name').val() !== '' && $('textarea#att-value').val() !==''){
        if (data_name.indexOf($('input#data-name').val())===-1){
            let section = "<tr id='"+gen_random_number()+"' class=\"tr-table\" ><td><fieldset><div class=\"vs-radio-con\">\n" +
                "<input type=\"checkbox\" id='"+'input#'+gen_random_number()+"' name=\"vueradio\" value=\"false\"><span class=\"vs-radio\">\n" +
                "<span class=\"vs-radio--border\"></span><span class=\"vs-radio--circle\"></span></span>\n" +
                "</div></fieldset></td><td class=\"dt-name\">"+$('input#data-name').val()+"</td><td>"+$('textarea#att-value').val()+"</td></tr>"
            $('#attr-table tbody').append(section)
            toastr.success('ویژگی محصول با موفقیت افزوده شد.', 'موفقیت آمیز!', {
                tapToDismiss: false,
                positionClass:"toast-top-center",
                progressBar:true,
            });

        }
        else{
            toastr.warning('ویژگی ای با این نام از قبل در لیست موجود است.', 'اخطار!', {
                tapToDismiss: false,
                positionClass:"toast-top-center",
                progressBar:true,
            });
        }
    }
    else{
        toastr.error('لطفا مقادیر را در ورودی ها وارد کنید', 'خطا!', {
            tapToDismiss: false,
            positionClass:"toast-top-center",
            progressBar:true,
        });
    }

})
$('button#remove-attr-btn').click(()=>{
    $.each($('#attr-table input[name="vueradio"]'),function (index,value){
        if ($(value).prop("checked")===true){
            $(value).parents("tr").first().remove()
        }
    })
})

$('#attr-table input[name="check-all"]').change(function(){
    if ($(this).prop("checked")===true){
        $.each($('#attr-table input[name="vueradio"]'),function () {
            $(this).prop('checked',true)
        })
    }else if($(this).prop("checked")===false){
        $.each($('#attr-table input[name="vueradio"]'),function () {
            $(this).prop('checked',false)
        })
    }
})
$('#attr-table input[name="search-attr"]').change(function () {
    const search_txt = $('#attr-table input[name="search-attr"]').val()
    let dt_list_found = []
    const re=new RegExp(search_txt)

    $.each($('#attr-table tr.tr-table'),function (index,value) {
        if(dt_list_found.indexOf($(value).prop("id"))=== -1){
            $(this).removeClass("d-none")
        }
    })

    $.each($('#attr-table td.dt-name'),function (index,value) {
        if ($(this).text().search(re) !== -1){
            dt_list_found.push($(this).parents("tr").first().prop("id"))
        }
    })

    $.each($('#attr-table tr.tr-table'),function (index,value) {
        if(dt_list_found.indexOf($(value).prop("id"))=== -1){
            $(this).addClass("d-none")
        }
    })
})
