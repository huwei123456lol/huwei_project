$(function(){
    var search = document.getElementById('search');
    search.addEventListener('click',function(){
        var searchValue = document.getElementById('searchValue').value;
        $.ajax({
            url:"default/search",
            type: "POST",
            data:{"ge_ming": searchValue},
            datatype: "json",
            success: function(){
                self.location="../display";
            }
        });
    });
    $("#ge_ming_list p").click(function(event){
        var ge_ming = event.target.innerText;
        $.ajax({
            url: "search",
            type: "POST",
            data: {"ge_ming": ge_ming},
            datatype: "json",
            success: function(){
                self.location="display/ge_ci";
            }
        });
    });
})