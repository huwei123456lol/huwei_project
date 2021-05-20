$(function(){
	$("span.updateuser").click(function(){
		$.ajax({
			url: "/admin/user/update",
			type: "POST",
			data: {"username": this.previousSibling.nodeValue},
			datatype: "json",
			success: function(data){
				alert(data);
				self.location = '/admin/user/updating';
			}
		});
	});
}());