#配置 发送邮箱

SECRET_KEY = 'wuihugehaghbjsbnwewu'


# 连接数据库：
# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名，读者用自己设置的
USERNAME = "root"
# 连接MySQL的密码，读者用自己的
PASSWORD = "548586"
# MySQL上创建的数据库名称
DATABASE = "zhiliaooa"

# 字符串前面加上字母"f"表示这是一个格式化字符串。格式化字符串允许在字符串中插入变量或表达式的值，使用大括号 "{}" 来表示插入点。
DB_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI=DB_URL



# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_USE_SSL=True  #是否加密
MAIL_PORT=465
MAIL_USERNAME='1494131966@qq.com'
MAIL_PASSWORD='esxznafemuhnghja'#开启SMTP服务器时生成的授权码
MAIL_DEFAULT_SENDER='1494131966@qq.com'


