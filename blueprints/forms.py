#注册表单
import wtforms
from wtforms.validators import Email,Length,EqualTo,InputRequired
from models import UserModel,EmailCaptchaModel
from exts import db


#表单Form:验证前端提交数据是否符合要求,,validators是验证器
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message='验证码格式错误')])
    username = wtforms.StringField(validators=[Length(min=3,max=20,message='用户名格式错误')])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message='密码格式错误')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password',message='两次密码不一致')])

    #自定义验证：
    # 1. 邮箱是否已被注册
    # 2. 验证码是否正确

    # 1. 邮箱是否已被注册
    def validate_eamil(self,field ):#filed 代表email这个字段
        email=field.data
        #会根据邮箱查询用户数据表，返回第一个匹配的用户对象（如果存在）
        user=UserModel.query.filter_by(email=email).first()
        #如果存在则提示
        if user:
            raise wtforms.ValidationError(message='邮箱已被注册')

    # 2. 验证码是否正确
    def validata_captcha(self, field):
        captcha=field.data
        email=self.email.data
        #找数据库中是否有相应的邮箱和验证码
        captcha_model=EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误')
        # else:
        # todo: 可以删掉captcha_model
        # 验证码用掉就会被删掉，但是会影响性能，会占用运行时间
        # db.session.delete(captcha_model)
        # db.session.commit()

class Loginform(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message='密码格式错误')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message='标题格式错误')])
    content = wtforms.StringField(validators=[Length(min=3,message='内容格式错误')])


class AnswerForm(wtforms.Form):
    content=wtforms.StringField(validators=[Length(min=3,message='内容格式错误')])
    question_id=wtforms.IntegerField(validators=[InputRequired(message='必须要传入问题id！')])