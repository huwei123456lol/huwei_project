$(function(){
    var cancle = document.getElementById("cancle");
    cancle.addEventListener('click',function(){
        self.location = "login";
    });
     var img = document.getElementById("img");
     var myImg = document.getElementById("myImg");
     myImg.onchange=function(){
        var reader = new FileReader();
        var file = myImg.files[0]; // fileobject
        reader.readAsDataURL(file);
        reader.onload=function(){
            $.ajax({
                url: "imgdir",
                type: "POST",
                data: {"img": this.result},
                datatype: "json",
                success: function(data){
                    img.src = data;
                }
            });
        }
        reader.onerror=function(){
            alert(reader.error);
        }
     }
    var submit = document.getElementById("submit");
    submit.addEventListener('click', function(){
        //  验证用户名是否含有非法字符
        var username = document.getElementById("username");
        var usernameValue = username.value.trim();
        if (usernameValue.search(/\s/i) != -1 || usernameValue.search(/[&^@#$~/><:;\\]/i) != -1){
            username.value = "";
            alert("用户名含有非法字符，请重新输入");
        }
        // 先验证密码是否含有非法字符，再验证密码是否相等，是否含有非法字符等 如空格等
        else{
            var password = document.getElementById("password");
            var passwordValue = password.value;
            if (passwordValue.search(/\s/i) != -1 || usernameValue.search(/[&^@#$~/><:;\\]/i) != -1){
                password.value = "";
                alert("密码含有非法字符，请重新输入");
            }
            else{
                var passwordAgain = document.getElementById("passwordAgain");
                var passwordAgainValue = passwordAgain.value;
                if(passwordValue !== passwordAgainValue){
                    passwordAgain.value = "";
                    alert("两次密码不相等，请重新输入");
                }
                else{
                    var name = document.getElementById("name").value;
                    var birthday = document.getElementById("birthday").value;
                    var nan = document.getElementById("nan").checked;
                    var sex = (nan==true)?"男":"女";
                    var email = document.getElementById("email").value;
                    var phone = document.getElementById("phone").value;
                    var aihao = document.getElementById("aihao").value;
                    // 提交数据
                    $.ajax({
                        url: "check",
                        type: "POST",
                        data:  {"username": usernameValue, "password": passwordValue, "myImg": img.src, "name": name, "birthday": birthday, "sex": sex, "email": email, "phone": phone, "aihao": aihao},
                        datatype: "json",
                        success: function(data){
                            alert(data);
                            if(data.search("已存在") != -1){
                                self.location = "register";
                            }
                            else{
                                self.location = "login";
                            }
                        }
                    });
                }
            }
        }
    });
})