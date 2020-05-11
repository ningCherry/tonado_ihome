import os

# Application配置参数
current_path = os.path.dirname(__file__)
settings=dict(
        static_path=os.path.join(current_path,'static')  #通过向web.Application类的构造函数传递一个名为static_path的参数来告诉Tornado从文件系统的一个特定位置提供静态文件
        ,template_path=os.path.join(current_path,'template')
        ,debug=True
        #import base64, uuid
        #base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)  ----这样得到的cookie_secret的一个值
        ,cookie_secret='nvgxOcQGREKyKzxs418MOqdHHV9EnE3kuCrTqmgaXtU='   #设置混淆秘钥，安全cookie用到
        ,xsrf_cookies=True   #开启XSRF保护
        # ,xsrf_cookies=False   #关闭XSRF保护
    )

# 数据库配置参数
mysql_options=dict(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='mysql123',
    db='ihome'
)

# Redis配置参数
redis_options=dict(
    host='127.0.0.1',
    port=6379
)

# 日志配置
log_path = os.path.join(current_path, "logs/log")
log_level = "debug"

# 密码加密密钥
passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="