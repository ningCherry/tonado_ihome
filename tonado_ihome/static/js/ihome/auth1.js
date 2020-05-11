function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function(){
    $.get('/api/profile/auth',function(data){
        if('4101'==data.errcode){
            location.href = "/login.html";
        }
        else if('0'== data.errcode){
            if(data.data.real_name && data.data.id_card){
                $('#real-name').val(data.data.real_name);
                $('#id-card').val(data.data.id_card);
                $('#real-name').prop('disabled', true);
                $('#id-card').prop('disabled', true);
                $('.btn-success').hide()
            }
        }
    }, "json");

    $('#form-auth').submit(function(e){
        e.preventDefault();

        if ($("#real-name").val()=="" || $("#id-card").val() == "") {
            $(".error-msg").show();
        }

        var data={};
        $(this).serializeArray().map(function(x){data[x.name] = x.value;});
        var jsonData = JSON.stringify(data);
        $.ajax({
            url:'/api/profile/auth',
            type:'POST',
            data:jsonData,
            contentType:'application/json',
            dataType:'json',
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            }
        })
        .done(function(data){
            if('0'==data.errcode){
                showSuccessMsg();
                $('#real-name').prop('disabled',true);
                $('#id-card').prop('disabled',true);
                $('.btn-success').hide();
            }
        })
    })
})