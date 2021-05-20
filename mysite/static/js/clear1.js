$(function(){
	cancle = document.getElementById("cancle");
	cancle.addEventListener("click",function(){
		username = document.getElementById("username");
		password = document.getElementById("password");
		username.value = "";
		password.value = "";
	});
}());