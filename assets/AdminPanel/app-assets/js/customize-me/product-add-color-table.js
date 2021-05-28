$('button#add-color-btn').click(function () {
    $("#add-color-sidebar").children("div.overlay-bg").toggleClass("show")
    $("#add-color-sidebar").children('div.add-new-data').toggleClass("show")
})


$('#ColorInput').spectrum({
    type: "component",
    showAlpha: false,
    allowEmpty: false,
    chooseText: "انتخاب",
});
$(document).ready(function () {
    $("button.sp-cancel").text("انصراف")
})

let counter_color = 0
$("#add-color-btn-form").click(function () {
    if (counter_color <= 4) {
        let has_color = []
        $.each($("#table-body-content tr"), function () {
            has_color.push($(this).children("td.td-color-code").text())
        })
        if (has_color.indexOf($("input#ColorInput").val()) === -1) {
            let input_td = `<td scope="row">
                                                                                <fieldset>
                                                                                    <div class="vs-radio-con">
                                                                                        <input id="select_${$("input#ColorInput").val().replace("#", "")}" type="checkbox"
                                                                                               name="check-all"
                                                                                               value="false">
                                                                                        <span class="vs-radio">
                                                            <span class="vs-radio--border"></span>
                                                            <span class="vs-radio--circle"></span>
                                                            </span>
                                                                                    </div>
                                                                                </fieldset>
                                                                            </td>`
            let color_code_td = `<td class="td-color-code">${$("input#ColorInput").val()}</td>`
            let color_td = `<td class="td-color"><i class="fa fa-square font-size-large" style="color: ${$("input#ColorInput").val()}"></i></td>`
            $("#table-body-content").append("<tr>" + input_td + color_code_td + color_td + "</tr>")
            counter_color += 1
            toastr.success('رنگ محصول با موفقیت افزوده شد.', 'موفقیت آمیز!', {
                tapToDismiss: false,
                positionClass: "toast-top-center",
                progressBar: true,
            });
        } else {
            toastr.error('رنگ محصول از قبل داخل لیست موجود است!', 'خطا!', {
                tapToDismiss: false,
                positionClass: "toast-top-center",
                progressBar: true,
            });
        }
    } else {
        toastr.error('محصول نمیتواند بیشتر از 5 رنگ داشته باشد!', 'خطا!', {
            tapToDismiss: false,
            positionClass: "toast-top-center",
            progressBar: true,
        });
    }
})

//Remove From Table 
$("#remove-color-btn").click(function () {
    $.each($("#table-body-content tr input:checked"),function (){
        $(this).parents("tr").first().remove()
    })
})
$('#color-table input[name="check-all"]').change(function () {
    if ($(this).prop("checked")===true){
        $.each($('#table-body-content tr input'),function () {
            $(this).prop('checked',true)
        })
    }else{
        $.each($('#table-body-content tr input'),function () {
            $(this).prop('checked',false)
        })
    }
})
