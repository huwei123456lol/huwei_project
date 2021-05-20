$(function(){
	$("span.addtable").click(function(){
		self.location = "/admin/table";
	});
	$("span.adduser").click(function(){
		self.location = "/admin/user";
	});
	$("span.addData").click(function(){
		self.location = "/admin/table/data/add";
	});
	$("span.lookData").click(function(){
		self.location = "/admin/table/data/look";
	});
}());