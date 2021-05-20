$(function(){
    $("#infoId").hide();
    var submit = document.getElementById("submit");
    var cancle = document.getElementById("cancle");
    cancle.addEventListener('click', function(){
        self.location = "../user/login";
    });
    submit.addEventListener('click', function(){
        var id = document.getElementById('infoId').innerText;
        var name = document.getElementById('name').value;
        var birthday = document.getElementById('birthday').value;
        var sex = document.getElementById('sex').value;
        if(sex!="男" && sex!="女"){
            alert("性别错误，重新输入");
            return;
        }
        var email = document.getElementById('email').value;
        var phone = document.getElementById('phone').value;
        var ai_hao = document.getElementById('aihao').value;
        $.ajax({
            url: "update",
            type: "POST",
            data: {"id": id, "name": name, "birthday": birthday, "sex": sex, "email": email, "phone": phone, "aihao": ai_hao},
            datatype: "json",
            success: function(data){
                alert(data);
                self.location = "../user/login";
            }
        });
    });
})