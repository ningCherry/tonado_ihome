//获取指定Cookie的函数，获取_xsrf
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function showSuccessMsg(){
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

$(function(){
    $.get('/api/profile',function(data){
        if("4101" == data.errcode){
            location.href='/login.html'
        }
        else{
            $('#user-name').val(data.data.name);
            if (data.data.avatar){
                $("#user-avatar").attr("src", data.data.avatar+'.png');
            }
        }
    });

    $('#form-name').submit(function(e){
        e.preventDefault();

        $('.image_uploading').fadeIn('fast');
        var options={
            url:'/api/profile/avatar',
            type:'POST',
            //dataType:'json',
            //data:{'_xsrf':getCookie("_xsrf")},
            headers: {
                "X-XSRFTOKEN": getCookie("_xsrf"),    //这里写了xsrf，不知道为啥还报错 '_xsrf' argument missing from POST
            },
            success: function(data){
                if('0'==data.errcode){
                    $('.image_uploading').fadeOut('fast');
                    $("#user-avatar").attr("src", data.data)
                }
                else if("4101" == data.errcode) {
                    location.href = "/login.html";
                }
            }
        };
        $(this).ajaxSubmit(options);

           //上传图片，试了下用$.post不行。要用上面$(this).ajaxSubmit()方法
//        $.post('/api/profile/avatar',"_xsrf="+getCookie("_xsrf"),function(data){
//            if('0'==data.errcode){
//                $('.image_uploading').fadeOut('fast');
//                $("#user-avatar").attr("src", data.data)
//                }
//                else if("4101" == data.errcode) {
//                    location.href = "/login.html";
//                }
//        })

    });

    $('#form-name').submit(function(e){
        e.preventDefault();

        var data={};
        $(this).serializeArray().map(function(x){data[x.name] = x.value;});
        var jsonData=JSON.stringify(data);
        $.ajax({
            url:'/api/profile/name',
            type:'POST',
            data:jsonData,
            contentType:'application/json',
            dataType: "json",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            }
        })
        .done(function(data){
            if('0'==data.errcode){
                $(".error-msg").hide();
                showSuccessMsg(); // 展示保存成功的页面效果
            }
            else if("4001" == data.errcode){
                $(".error-msg").show();
            }
            else if("4101" == data.errcode){   // 4101代表用户未登录，强制跳转到登录页面
                location.href = "/login.html";
            }
            else{
                $('.error-msg').html('不能为空！')
                $(".error-msg").show();
            }
        })
    })
})