$(function(){
    $("#ge_ming p").click(function(event){
        var data = event.target.innerText;
        $.ajax({
            url: "../search",
            type: "POST",
            data: {"ge_ming": data},
            datatype: "json",
            success: function(){
                self.location="../display/ge_ci";
            }
        });
    });
})