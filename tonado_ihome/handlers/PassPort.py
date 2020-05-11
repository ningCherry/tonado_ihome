from .BaseHandler import BaseHandler
import logging
import re
import hashlib
import pymysql

from utils.response_code import RET
import config
from utils.session import Session

db = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='mysql123', db='ihome')
cursor = db.cursor()

"""注册"""
class RegisterHandler(BaseHandler):
    # def get(self):
    #     logging.debug('debug info')
    #     logging.info('info info')
    #     logging.warning('warning info')
    #     logging.error('error info')
    #     self.write('hello')

    def post(self):
        # 获取参数
        mobile=self.json_args.get('mobile')
        sms_code = self.json_args.get("phonecode")
        password = self.json_args.get("password")
        print(mobile, sms_code, password)

        # 检查参数
        if not all((mobile, sms_code, password)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))

        if not re.match(r'^1\d{10}$',mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号格式错误"))

        # 如果产品对于密码长度有限制，需要在此做判断
        # if len(password)<6

        # 判断短信验证码是否正确
        if sms_code!='2468':    #设置万能短信验证码
            try:
                real_sms_code=self.redis.get("sms_code_%s" % mobile)
                # print(real_sms_code.decode('utf-8'))
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR, errmsg="查询验证码出错"))

            # 判断短信验证码是否过期
            if not real_sms_code:
                return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))

            # 对比用户填写的验证码与真实值
            if real_sms_code.decode('utf-8')!=sms_code:
                return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))

            try:
                self.redis.delete("sms_code_%s" % mobile)
            except Exception as e:
                logging.error(e)

        # 保存数据，同时判断手机号是否存在，判断的依据是数据库中mobile字段的唯一约束
        # password = hashlib.sha256(password+ config.passwd_hash_key).hexdigest()  #报错，有时间再研究加密吧

        # sql = "insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%(name)s, %(mobile)s, %(passwd)s);"   #不要这样写，会报错，不知道为什么
        sql="insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%s,%s,%s);"  #防止sql注入
        # sql="insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%s, %s, %s);"%(mobile,mobile,password)
        print(sql)
        try:
            # user_id=self.db.cursor().execute(sql)   #不知道为什么用self.db，数据库为什么没有插入数据，有时间再研究吧。见https://www.cnblogs.com/cherry-ning/articles/12635856.html
            # user_id=cursor.execute(sql)
            user_id =cursor.executemany(sql,[(mobile,mobile,password)])  #防止sql注入
            # print(user_id) #user_id=1
            db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAEXIST, errmsg="手机号已存在"))

        # 用session记录用户的登录状态
        session=Session(self)
        session.data['user_id']=user_id
        session.data['mobile']=mobile
        session.data['name']=mobile
        # print(session.session_id)
        # print(session.data)
        try:
            session.save()
        except Exception as e:
            logging.error(e)

        self.write(dict(errcode=RET.OK, errmsg="注册成功"))


"""登录"""
class LoginHandler(BaseHandler):
    def post(self):
        # 获取参数
        mobile=self.json_args.get('mobile')
        password=self.json_args.get('password')

        # 检查参数
        if not all([mobile,password]):
            return self.write(dict(errcode=RET.PARAMERR,errmsg='参数不正确'))
        if not re.match(r'^1\d{10}$',mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号错误"))

        sql='select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%s'
        cursor.executemany(sql,[(mobile,)])
        res=cursor.fetchone()
        print(res)  #例：(87, '15801801915', '1')

        # 检查用户是否存在及密码是否正确
        if res and res[2]==password:
            try:
                # 生成session数据
                # 返回客户端
                self.session=Session(self)
                self.session.data['user_id']=res[0]
                self.session.data['name']=res[1]
                self.session.data['mobile']=mobile
                self.session.save()
                print(self.session.data)
            except Exception as e:
                logging.error(e)
            return self.write(dict(errcode=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号或密码错误！"))


class LogoutHandler(BaseHandler):
    """退出登录"""
    def get(self):
        self.session=Session(self)
        # 清除session数据
        self.session.clear()
        self.write(dict(errcode=RET.OK, errmsg="退出成功"))


class CheckLoginHandler(BaseHandler):
    """检查登陆状态"""
    def get(self):
        # get_current_user方法在基类中已实现，它的返回值是session.data（用户保存在redis中
        # 的session数据），如果为{} ，意味着用户未登录;否则，代表用户已登录
        if self.get_current_user():
            self.write({"errcode": RET.OK, "errmsg": "true", "data": {"name": self.session.data.get("name")}})
        else:
            self.write({"errcode": RET.SESSIONERR, "errmsg": "false"})





