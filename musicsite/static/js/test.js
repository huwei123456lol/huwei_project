$(function (){
    test_context = document.getElementById("test");
    test_btn = document.getElementById('test_btn');
    test_btn.addEventListener("click",function(){
		$.ajax({
			url: "default/search",
			type: "POST",
			data: {"ge_ming": "香女人"},
			datatype: "json",
			success: function(){
                self.location="default/test";
			}
		});
	});
})