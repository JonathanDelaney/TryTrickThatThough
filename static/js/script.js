$(window).bind('load', function() {
    $(".spinner-border").css("display", "none");
    $(".spinner-cont").css("height", "0px");
});

// $('form').hover(function() {
//     let coords = $('input[type=hidden]', this).val();
//     console.log(coords);
//     $(this).append("<div id='tooltip-box'>" + coords + "</div>");
//     }, function () {
//     $("div#tooltip-box").remove();
// })