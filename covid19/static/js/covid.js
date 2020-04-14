function showMessage() {
    $('.up').show()
    $('.btn').attr('disabled', 'disabled');
    //document.getElementsByClassName("btn").style.visibility = "hidden";
    document.getElementsByClassName("btn").disabled = true;
    var x = document.getElementById("listid");
        x.style.opacity = "0.2";
        //x.style.cursor = "default"; 
        //x.style.pointer-events = "none";
        //x.style.display = "none";
        $(document).ready(function(){
            $('form button[type="submit"]').prop("disabled", true);
        });
}

/*
$('.btn').attr('disabled', true); 
$('.fas').attr('disabled', true); 
$('.btn').attr('disabled', 'disabled');
$('.fas').attr('disabled', 'disabled');
*/
//$('form button[type="submit"]').prop("disabled", true);
