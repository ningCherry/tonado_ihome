//获取指定Cookie的函数，获取_xsrf
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId="";

function generateUUID(){
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode(){
    var picId=generateUUID();
    $('.image-code img').attr("src","/api/piccode?pre="+imageCodeId+"&cur="+picId);
    imageCodeId=picId;
}

function sendSMSCode(){
    $('.phonecode-a').removeAttr('onclick');
    var mobile=$('#mobile').val();
    if(!mobile){
        $('#mobile-err span').html('请填写手机号码！');
        $('#mobile-err').show();
        $('.phonecode-a').attr('onclick','sendSMSCode();');
        return;
    }
    var imgcode=$('#imagecode').val();
    if(!imgcode){
        $('#image-code-err span').html("请填写图形验证码");
        $('#image-code-err').show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    var data={mobile:mobile,piccode:imgcode,piccode_id:imageCodeId};
    $.ajax({
        url:'/api/smscode',
        type:'POST',
        dataType:'json',
        data: JSON.stringify(data),
        contentType:'application/json',
        headers:''
    })
    .done(function(data){
        if('0'==data.errcode){
            var duration = 60;
            var timeObj = setInterval(function () {
                duration = duration - 1;
                $(".phonecode-a").html(duration+"秒");
                if (1 == duration) {
                    clearInterval(timeObj)
                    $(".phonecode-a").html("获取验证码");
                    $(".phonecode-a").attr("onclick", "sendSMSCode();");
                }
            }, 1000, 60)
        }
        else{
            $('#image-code-err span').html(data.errmsg);
            $('#image-code-err').show();
            $('.phonecode-a').attr('onclick','sendSMSCode();');
            if(data.errcode=='4002' || data.errcode=='4004'){
               generateImageCode();
            }
        }
    })
}

$(document).ready(function(){
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $('#imagecode').focus(function(){
        $('#image-code-err').hide();
    });
    $('#phonecode').focus(function(){
        $('#phone-code-err').hide();
    });
    $('#password').focus(function(){
        $('#password-err').hide();
        $('#password2-err').hide();
    });
    $('#password2').focus(function(){
        $('#password2-err').hide();
    });

    // 当用户点击表单提交按钮时执行自己定义的函数
    $('.form-register').submit(function(e){
        // 组织浏览器对于表单的默认行为
        e.preventDefault();

        // 校验用户填写的参数
        mobile=$('#mobile').val();
        phonecode=$('#phonecode').val();
        password=$('#password').val();
        password2=$('#password2').val();

        if(!mobile){
            $('#mobile-err span').html("请填写正确的手机号！");
            $('#mobile-err').show();
            return;
        };
        if(!phonecode){
            $('#phone-code-err span').html("请填写短信验证码！");
            $('#phone-code-err').show();
            return
        };
        if(!password){
            $('#password-err span').html("请填写密码！");
            $('#password-err').show();
            return;
        };
        if(password != password2){
            $('#password2-err span').html("两次密码不一致！");
            $('#password2-err').show();
            return;
        };

        // 把表单中的数据填充到data中
        var data={mobile:mobile,phonecode:phonecode,password:password}   //这样写可以
        //var data={"mobile":mobile,"phonecode":phonecode,"password":password}   //这样写也行

//        var data={};   // 声明一个要保存结果的变量
//        $(".form-register").serializeArray().map(function(x){data[x.name]=x.value})  //这样写也行
        // 把data变量转为josn格式字符串
        var json_data = JSON.stringify(data)
        //向后端发送请求
        $.ajax({
            url:'/api/register',
            type:'POST',
            data: json_data,
            contentType: "application/json", // 告诉后端服务器，发送的请求数据是json格式的
            dataType:'json',  // 告诉前端，收到的响应数据是json格式的
            headers: {
                "X-XSRFTOKEN": getCookie("_xsrf"),
            }
        })
        .done(function(data){
            if("0"==data.errcode){
                location.href='/';
            }
            else if("验证码过期" == data.errmsg || "验证码错误" == data.errmsg){
                $("#phone-code-err>span").html(data.errmsg);
                $("#phone-code-err").show();
            }
        })
    })

})