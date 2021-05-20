$(function(){
    var submit = document.getElementById('submit');
    var cancle = document.getElementById('cancle');
    var register = document.getElementById('register');
    submit.addEventListener('click',function(){
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        $.ajax({
            url:"info",
            type: "POST",
            data:{"username": username, "password": password},
            datatype: "json",
            success: function(data){
                if (data=='user error'){
                    alert("用户名错误！");
                }
                else if( data=='password error'){
                    alert("密码错误！");
                }
                else{
                    self.location='index';
                }
            }
        });
    });
    cancle.addEventListener('click',function(){
        self.location="../..";
    });
    register.addEventListener('click',function(){
        self.location="register";
    });
})