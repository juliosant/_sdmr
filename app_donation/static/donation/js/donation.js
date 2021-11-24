function lowerWord(e) {
    var ss = e.target.selectionStart;
    var se = e.target.selectionEnd;
    e.target.value = e.target.value.toLowerCase();
    e.target.selectionStart = ss;
    e.target.selectionEnd = se;
 }


$(window).ready(function() {
    $("#donation").on("keypress", function (event) {
        //console.log("aaya");
        var keyPressed = event.keyCode || event.which;
        if (keyPressed === 13) {
            //alert("You pressed the Enter key!!");
            event.preventDefault();
            return false;
        }
    });
});

