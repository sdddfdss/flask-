# 授权相关的

# 创建蓝图
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm, Loginform
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


# /auth/login
# 登录
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':  # 渲染页面
        return render_template('login.html')
    else:  # POST
        form = Loginform(request.form)
        if form.validate():  # 验证
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print('邮箱在数据库中不存在')
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                # cookie: 不适合储存太多数据，只适合存储少量的数据
                # cookie一般用来存放登录授权的东西
                # flask中的session，是经过加密后存储在cookie中的
                session['user_id'] = user.id
                return redirect('/')  # 返回首页
            else:
                print('密码错误!')  # 登录失败
                return redirect(url_for('auth.login'))

        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


# 退出登录
@bp.route('logout')
def logout():
    session.clear()
    return redirect('/')  # 返回到首页


# 渲染
# GET：从服务器获取数据（获取html代码）
# POST：将客户端的数据提交给服务器（将注册信息提交给服务器）
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # 验证码和邮箱是否对应   （最好将验证码存在服务器中）
        # 表单验证:flask-wtf:wtforms
        return render_template('register.html')
    else:
        # 获取前端提交的数据（邮箱等等） 再验证
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))  # 密码需要加密
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))  # 跳转到登录页面
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))  # 跳转页面


# 没指定methods参数默认就是GET请求
# 发送验证码
@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get('email')  # 获取？后面的邮箱email=932423029@qq.com
    # 4/6 随机数组，字母，数组和字母组合
    source = string.digits * 4  # 0123456789012345678901234567890123456789
    captcha = random.sample(source, 4)  # 随机选取四位数
    print(captcha)
    captcha = ''.join(captcha)  # 将列表中的元素连接在一起
    # 发送邮件
    # I/O:input/output  耗时操作，致使点了”获取验证码“后需要等一会儿才会开始倒计时
    message = Message(subject='知了传课注册验证码', recipients=[email], body=f'您的验证码是{captcha}')
    mail.send(message)

    # memcached/redis 大型项目存储在服务器上
    # 用数据库存储验证码
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    return jsonify({'code': 200, 'message': '', 'data': None})


# 测试
@bp.route('/mail/test')
def mail_test():
    message = Message(subject='邮箱测试', recipients=['932423029@qq.com'], body='测试')
    mail.send(message)
    return '邮件发送成功'
