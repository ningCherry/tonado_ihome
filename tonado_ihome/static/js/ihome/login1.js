//获取指定Cookie的函数，获取_xsrf
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function(){
    $('#mobile').click(function(){
        $('#mobile-err').hide();
    });
    $('#password').click(function(){
        $('#password-err').hide();
    });

    $('.form-login').submit(function(e){
        e.preventDefault();

        mobile=$('#mobile').val();
        password=$('#password').val();
        if(mobile==''){
            $('#mobile-err span').html('请填写正确的手机号码！');
            $('#mobile-err').show();
            return;
        }
        if(password==''){
            $('#password-err span').html('请填写正确的手机号码！');
            $('password-err').show();
            return;
        }

        //请求体是json格式，需通过设置HTTP头X-XSRFToken来传递_xsrf值。详见https://www.cnblogs.com/cherry-ning/articles/12642909.html
        var data={'mobile':mobile,'password':password}
        //var data={mobile:mobile,password:password}   //这样写可以

        //var data={};   // 声明一个要保存结果的变量
        //$(".form-login").serializeArray().map(function(x){data[x.name]=x.value})  //这样写也行
        var jsondata=JSON.stringify(data)
        $.ajax({
            url:'/api/login',
            type:'POST',
            data:jsondata,
            dataType:'json',
            contentType:'application/json',
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            }
        })
        .done(function(data){
            if('0'==data.errcode){
                location.href='/';
                return;
            }
            else{
                $('#password-err span').html(data.errmsg);
                $('#password-err').show();
                return;
            }
        });


        //试过用$.post(,,function(data))方法不行，请求体是其他格式的（如json或xml等），必须通过设置HTTP头X-XSRFToken来传递_xsrf值。$.post不知道怎么设置请求头，所以还是用$.ajax({})吧
//        var xsrf = getCookie("_xsrf");
//        //var data1={'mobile':mobile,'password':password,'_xsrf':xsrf}
//        var data1={'mobile':mobile,'password':password}
//        var jsondata=JSON.stringify(data1)
//        $.post('/api/login', "_xsrf="+xsrf+'&'+jsondata,function(data){
//        //$.post('/api/login', jsondata,function(data){
//            if('0'==data.errcode){
//                location.href='/';
//                return;
//            }
//            else{
//                $('#password-err span').html(data.errmsg);
//                $('#password-err').show();
//                return;
//            }
//        });

    });
})