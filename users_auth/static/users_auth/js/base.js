function upperWord(e) {
    //var x = document.getElementById(id);
    //x.value = x.value.toUpperCase();
    var ss = e.target.selectionStart;
    var se = e.target.selectionEnd;
    e.target.value = e.target.value.toUpperCase();
    e.target.selectionStart = ss;
    e.target.selectionEnd = se;
}

function lowerWord(e) {
    var ss = e.target.selectionStart;
    var se = e.target.selectionEnd;
    e.target.value = e.target.value.toLowerCase();
    e.target.selectionStart = ss;
    e.target.selectionEnd = se;
 }

$(window).ready(function() {
    $("#formRegister").on("keypress", function (event) {
        //console.log("aaya");
        var keyPressed = event.keyCode || event.which;
        if (keyPressed === 13) {
            //alert("You pressed the Enter key!!");
            event.preventDefault();
            return false;
        }
    });
});

$('inputTag').keydown(function(e) {
    if(e.which === 188 || e.which === 110) { // 188 é vírgula e 110 virgula do teclado numérico
        return false;   
        // ou:
        // e.preventDefault();
    }
});
