from tornado.web import RequestHandler,StaticFileHandler
import pymysql
import redis
import json

import config
from utils.session import Session

class BaseHandler(RequestHandler):
    @property  #创建只读属性,这样可以防止属性被修改
    def db(self):
        #mysql数据库
        mysql_options=pymysql.Connect(**config.mysql_options)
        # cursor=mysql_options.cursor()
        # return [mysql_options,cursor]
        return mysql_options

    @property
    def redis(self):
        #redis数据库
        redis_options=redis.StrictRedis(**config.redis_options)
        return redis_options

    def prepare(self):
        self.xsrf_token
        """预解析json数据"""
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args=json.loads(self.request.body)
        else:
            self.json_args={}

    def get_current_user(self):
        """判断用户是否登录"""
        self.session=Session(self)
        return self.session.data

    def write_error(self, status_code,**kwargs):
        pass

    def initialize(self):
        pass

    def set_default_headers(self):
        pass

    def on_finish(self):
        pass


#StaticFileHandler是tornado预置的用来提供静态资源文件的handler
class StaticFileBaseHandler(StaticFileHandler):
    """自定义静态文件处理类, 在用户获取html页面的时候设置_xsrf的cookie。见https://www.cnblogs.com/cherry-ning/articles/12642909.html"""
    def __init__(self,*args,**kwargs):
        super(StaticFileBaseHandler,self).__init__(*args,**kwargs)
        self.xsrf_token