$(function(){
	$("span.bgcolor").click(function(){
		$.ajax({
			url: "/admin/table/look",
			type: "post",
			data: {"tablename": this.previousSibling.nodeValue},
			datatype: "json",
			success: function(returnData){
				alert(returnData);
				self.location = "/admin/table/look";
			}
		});
	});
}());