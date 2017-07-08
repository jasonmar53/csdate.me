$("form").submit(function(e) {

    var ref = $(this).find("[required]");

    $(ref).each(function(){
        if ( $(this).val() == '' )
        {
            alert("Please fill all form fields.");

            $(this).focus();

            e.preventDefault();
            return false;
        }
    });  return true;
});
