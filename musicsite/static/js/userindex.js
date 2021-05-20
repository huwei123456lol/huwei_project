$(function(){
    var mainBody = document.getElementById("mainBody");
    var search = document.getElementById("search");
    var username = document.getElementById("username");
    search.addEventListener("click", function(){
        var searchValue = document.getElementById("searchValue").value;
        $.ajax({
            url: "search",
            type: "POST",
            data: {"ge_ming": searchValue},
            datatype: "json",
            success: function(data){
                mainBody.innerText="";
                var arr_value = data.split(",");
                var len = arr_value.length;
                for(var i=0;i<len;i++){
                    var p = document.createElement("p");
                    p.innerText=arr_value[i];
                    mainBody.appendChild(p);
                }
            }
        });
    });
    // 点击body中的页面进行查找歌曲
    mainBody.addEventListener('click', function(event){
        var ge_ming = event.target.innerText;
        if(ge_ming=="你还没有歌曲呐，请添加"){
            $.ajax({
                url: "../../searchBody",
                type: "GET",
                success: function(data){
                    mainBody.innerText="";
                    var value_random = data.split(",");
                    var len = value_random.length;
                    for(var i = 0 ; i < len;i++){
                        var p = document.createElement("p");
                        p.innerText=value_random[i];
                        mainBody.appendChild(p);
                    }
                }
            });
        }
        else{
            var myImg = document.getElementById("myImg");
            // 通过内部或外部数据库查找歌曲
            $.ajax({
                url: "find",
                type: "POST",
                data: {"ge_ming": ge_ming,"img": myImg.src, "username": username.innerText},
                datatype: "json",
                success: function(){
                    self.location="../user/sing";
                }
            });
        }
    });
    // 点击用户名获得用户的信息
    username.addEventListener('click', function(){
        $.ajax({
            url: "myInfo",
            type: "POST",
            data: {"username": username.innerText},
            datatype: "json",
            success: function(){
                self.location="../user/displayInfo";
            }
        });
    });
    //首先去掉浏览器右键自带属性
    /**
    document.oncontextmenu=function(event){
        event.preventDefault();
    }
    **/
    // 右点body中的歌名跳出一个快捷菜单，弹出一些快捷选项，比如我要添加等
    //这里有错误
    /**
    $("#mainBody p").mouseup(function(event){
        if(event.button == 2){
            $("#fastMenu").show();
            //选项选择
        }
    });
    **/
})