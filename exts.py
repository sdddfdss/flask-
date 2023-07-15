#扩展文件 插件
#exts.py 存在的意义是为了解决循环引用问题

from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

# 数据库对象，通常是一个 SQLAlchemy 实例。
db=SQLAlchemy()

mail=Mail()