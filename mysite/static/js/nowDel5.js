$(function(){
	$("span.deltable").click(function(){
		$.ajax({
			url: "/admin/table/del",
			type: "POST",
			data: {"tablename":this.previousSibling.previousSibling.nodeValue},
			datatype: "json",
			success:function(data){
				alert(data);
				self.location = "/admin/";
			}
		});
	});
	$("span.deluser").click(function(){
		$.ajax({
			url: "/admin/user/del",
			type: "POST",
			data: {"username":this.previousSibling.previousSibling.nodeValue},
			datatype: "json",
			success:function(data){
				alert(data);
				self.location = "/admin/";
			}
		});
	});
}());