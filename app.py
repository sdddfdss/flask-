# 汇总

from flask import Flask,session,g
import config
from exts import db , mail

# 从名为"models"的模块中导入"UserModel"类
from models import UserModel

from blueprints.qa import bp as qa_bp

from blueprints.auth import bp as auth_bp

# 数据库迁移管理。数据库迁移是指在应用程序的开发过程中，当需要修改数据库模型（例如添加新的表、修改表结构、删除表等）时，通过迁移脚本来保持数据库的同步。
from flask_migrate import Migrate

# 创建Flask应用程序实例
app = Flask(__name__)

# 绑定配置文件
app.config.from_object(config)

# 初始化数据库扩展,,db.init_app() 需要传递一个 Flask 应用程序对象作为参数
db.init_app(app)
mail.init_app(app)
# app 是 Flask 应用程序对象，即的 Flask 应用实例。
# db 是数据库对象，通常是一个 SQLAlchemy 实例。
migrate = Migrate(app, db)

# 注册蓝图
# 注册问答模块和认证模块的蓝图对象到应用程序中。蓝图用于模块化组织应用程序的路由和视图函数。
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# blueprint 蓝图:用来做模块化的
# 电影，音乐。。就是模块


#钩子函数 before_request/before_first_request/after_request

#before_request：在每个请求处理之前触发。该钩子函数适用于在处理请求之前进行一些通用的准备工作，例如验证用户身份、设置全局变量或执行其他预处理任务。
@app.before_request
def my_before_request():
    user_id=session.get('user_id')
    if user_id:
        user=UserModel.query.get(user_id)
        setattr(g,'user',user)
    else:
        setattr(g,'user',None)

#上下文处理器（在所有模板中可用）
@app.context_processor
def my_context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run()

# ORM模型映射成表的三步
# 1. flask db init 只需要执行一次
# 2. flask db migrate 识别ORM模型，生成迁移脚本
# 3. flask db upgrade 运行迁移脚本，同步到数据库中 *******
