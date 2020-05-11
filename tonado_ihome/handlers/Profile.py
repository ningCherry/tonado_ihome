from .BaseHandler import BaseHandler
from utils.commons import required_login
from utils.response_code import RET

import logging
import pymysql

db = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='mysql123', db='ihome')
cursor = db.cursor()

"""个人信息"""
class ProfileHandler(BaseHandler):
    @required_login
    def get(self):
        user_id=self.get_current_user()['user_id']
        print(user_id)
        sql='select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%s'
        try:
            cursor.executemany(sql, [(user_id,)])
            ret = cursor.fetchone()
            print(ret)
        except Exception as e:
            logging.error(e)
            return self.write({"errcode": RET.DBERR, "errmsg": "get data error"})
        self.write({"errcode":RET.OK, "errmsg":"OK",
                    "data":{"user_id":user_id, "name":ret[0], "mobile":ret[1], "avatar":ret[2]}})


"""上传头像"""
class AvatarHandler(BaseHandler):
    @required_login
    def post(self):
        files=self.request.files.get('avatar')
        if not files:
            return self.write(dict(errcode=RET.PARAMERR, errmsg="未传图片"))

        # 从session数据中取出user_id
        user_id = self.session.data['user_id']

        avatar=files[0]['body']  #获取图片用法见：https://www.cnblogs.com/cherry-ning/articles/12591376.html
        #保存图片
        filename=r'E:/python_practice_ku/tndo/tonado_ihome/static/upload/'+str(user_id)
        with open(filename+'.png','wb') as f:
            f.write(avatar)

        # 保存图片url到数据中
        sql='update ih_user_profile set up_avatar=%s where up_user_id=%s'
        filename1='/static/upload/'+str(user_id)
        # sql='update ih_user_profile set up_avatar="{}" where up_user_id={}'.format(filename1,user_id)
        print(sql)
        try:
            cursor.executemany(sql,[(filename1,user_id)])
            # cursor.execute(sql)
            db.commit()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="保存错误"))
        self.write(dict(errcode=RET.OK, errmsg="保存成功", data=filename1+'.png'))


"""用户名"""
class NameHandler(BaseHandler):
    @required_login
    def post(self):
        # 从session中获取用户身份,user_id
        user_id=self.session.data['user_id']

        # 获取用户想要设置的用户名
        name=self.json_args.get('name')

        # 判断name是否传了，并且不应为空字符串
        if not name:
            return self.write({"errcode":RET.PARAMERR, "errmsg":"params error"})

        # 保存用户昵称name，并同时判断name是否重复（利用数据库的唯一索引)
        sql='update ih_user_profile set up_name=%s where up_user_id=%s'
        try:
            cursor.executemany(sql,[(name,user_id)])
            db.commit()
        except Exception as e:
            logging.error(e)
            return self.write({"errcode":RET.DBERR, "errmsg":"name has exist"})

        # 修改session数据中的name字段，并保存到redis中
        self.session.data['name']=name
        try:
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write({"errcode": RET.OK, "errmsg": "OK"})


"""实名认证"""
class AuthHandler(BaseHandler):
    @required_login
    def get(self):
        # 在session中获取用户user_id
        user_id=self.session.data['user_id']

        # 在数据库中查询信息
        sql='select up_real_name,up_id_card from ih_user_profile where up_user_id=%s;'
        try:
            cursor.executemany(sql,[(user_id,)])
            ret=cursor.fetchone()
            # print(ret)
        except Exception as e:
            # 数据库查询出错
            logging.error(e)
            return self.write({"errcode":RET.DBERR, "errmsg":"get data failed"})
        if not ret:
            return self.write({"errcode": RET.NODATA, "errmsg": "no data"})

        self.write({"errcode": RET.OK, "errmsg": "OK","data" :{"real_name": ret[0], "id_card": ret[1]}})

    @required_login
    def post(self):
        user_id = self.session.data['user_id']
        real_name=self.json_args.get('real_name')
        id_card=self.json_args.get('id_card')
        print(real_name,id_card)

        if not all([real_name,id_card]):
            return self.write({"errcode":RET.PARAMERR, "errmsg":"params error"})

        # 判断身份证号格式

        sql='update ih_user_profile set up_real_name=%s,up_id_card=%s where up_user_id=%s;'
        print(sql)
        try:
            cursor.executemany(sql,[(real_name,id_card,user_id)])
            db.commit()
        except Exception as e:
            logging.error(e)
            return self.write({"errcode": RET.DBERR, "errmsg": "update failed"})
        self.write({"errcode": RET.OK, "errmsg": "OK"})
