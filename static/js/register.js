//将获取输入框邮箱进行发送验证码的操作放置在一个函数中，以便于后续再次绑定点击事件
function bindEmailCaptchaClick(){
    // “captcha-btn”是“获取验证码”这个按钮的id,绑定点击事件
    $("#captcha-btn").click(function(event){
        //  $this:j代表的是当前按钮的query对象
        var $this=$(this)
        // 阻止默认事件                            /*click点击之后会执行里面的函数*/
        event.preventDefault();
        // 获取名为"email"的输入框的值,并将其作为参数添加到发送验证码的URL中
        var email = $("input[name='email']").val();
        // 使用$.ajax()函数进行异步请求，向指定的URL发送GET请求
        $.ajax({
            url:"/auth/captcha/email?email=" + email,
            method:'GET',
            success:function (result){
                var code = result['code']
                if (code==200){
                    //倒计时为60秒
                    var countdown=5;
                    //开始倒计时之前，就取消按钮的点击事件
                    $this.off('click');
                    // setInterval 按照指定的时间间隔（以毫秒为单位）重复执行指定的函数或代码块。
                    var timer=setInterval(function (){
                        //将按钮的文字改为 countdown的值
                        $this.text(countdown);
                        countdown-=1
                        if(countdown <=0){
                            //清理掉定时器 就不会倒计时了
                            //setInterval()函数会一直重复执行，直到调用clearInterval()函数停止它
                            clearInterval(timer);
                            //将按钮的名字修改回来
                            $this.text('获取验证码');
                            //重新绑定点击事件,再次执行这个函数
                            bindEmailCaptchaClick();
                        }
                    },1000)  /*单位为毫秒  1000毫秒=1秒*/
                    alert('邮箱验证码发送成功');
                }else{
                    alert(result['message']);
                }
                console.log(result);  /*如果请求成功，success回调函数将被调用，并将返回的结果打印到控制台中(result)*/
            },
            fail:function (error){
                console.log(error); /*如果请求失败，fail回调函数将被调用，并将错误信息打印到控制台中*/
            }
        })
    })
}



//等整个网页加载后再执行
$(function(){
    bindEmailCaptchaClick();
})


//只有将数据库里面的账号，验证码数据删除才会出现倒计时
//如果数据库里面有一列为空值，并且也没有传入，那么倒计时就不会出现