$('.tic-button').click(function(){
        console.log("JS working")
    if ($('.player-turn').text() == "Guest's turn") {
        console.log("guest")
        //pass
    } else {
        $(this).css('background-color', 'rgb(197, 63, 45)');
        console.log("player 1")
    }
});