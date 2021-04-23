$(window).bind('load', function() {
    $(".spinner-border").css("display", "none");
    $(".spinner-cont").css("height", "0px");
    // $(".space-bg").css("display", "block");
});

$('.tic-button').click(function(){
        console.log("JS working")
    if ($('.player-turn').text() == "Guest's turn") {
        console.log("guest")
        //pass
    } else {
        $(this).css({'background-color': 'rgb(255, 103, 82)', 'filter': 'brightness(150%)'});
        // $(this).prop('disabled', true);
        console.log("player 1")
    }
});