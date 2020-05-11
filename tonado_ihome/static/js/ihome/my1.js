function logout(){
    $.get('/api/logout',function(data){
        if('0'==data.errcode){
            location.href = "/";
        }
    })
}

$(function(){
    $.get('/api/profile',function(data){
        if(data.errcode=='4101'){
            location.href='/login.html'
        }
        else{
            $('#user-name').html(data.data.name)
            $('#user-mobile').html(data.data.mobile)
            if(data.data.avatar){
                $('#user-avatar').attr('src',data.data.avatar+'.png');
            }
        }
    })
})