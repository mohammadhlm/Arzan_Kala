
<!--    Overlay Icon-->
$('span.img-hover-section').hover(function () {
    $(this).children("img.img-ch-photo-logo").toggleClass("img-hover-ch-photo")
    $(this).children("i").toggleClass("hidden-ch-photo-icon")
})
//Click Site Logo
$('#inp-ch-fv-icon-btn').click(function () {
    $('input#inp-ch-fv-icon').click()
})
$('#inp-ch-logo-head-site-btn').click(function () {
    $('input#inp-ch-logo-head-site').click()
})
$('#inp-ch-logo-foot-site-btn').click(function () {
    $('#inp-ch-logo-foot-site').click()
})

//    Click Brand Input
$('span#span-1-logo').click(function () {
    $('#logo-1').click()
})
$('span#span-2-logo').click(function () {
    $('#logo-2').click()
})
$('span#span-3-logo').click(function () {
    $('#logo-3').click()
})
$('span#span-4-logo').click(function () {
    $('#logo-4').click()
})
$('span#span-5-logo').click(function () {
    $('#logo-5').click()
})
