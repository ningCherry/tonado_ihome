# coding:utf-8

import uuid
import json
import logging

from constants import SESSION_EXPIRES_SECONDS

class Session():
    def __init__(self,request_handler):
        # 先判断用户是否已经有了session_id
        self._request_handler=request_handler
        self.session_id=self._request_handler.get_secure_cookie('session_id')  #有值的情况，这里得到的session_id应该是gbk格式。ps:首次注册，self.session_id无值，转码会报错

        # 如果不存在session_id,生成session_id
        if not self.session_id:
            self.session_id=uuid.uuid4().hex.encode('gbk')   #这几个转码坑死了，self.session_id无论存不存在，都转成gbk格式，为第36行服务
            print(self.session_id)
            self.data={}
            self._request_handler.set_secure_cookie("session_id", self.session_id)
        else:   # 如果存在session_id, 去redis中取出data
            try:
                json_data=self._request_handler.redis.get("sess_%s" % self.session_id)
            except Exception as e:
                logging.error(e)
                raise e
            if not json_data:
                self.data = {}
            else:
                self.data=json.loads(json_data.decode('utf-8'))  #这几个转码坑死了。redis查出来的必须要decode()
                # print(self.data)

    def save(self):
        json_data=json.dumps(self.data)
        try:
            self._request_handler.redis.setex("sess_%s" % self.session_id,SESSION_EXPIRES_SECONDS, json_data)  #这里的self.session_id，设置成gbk格式
        except Exception as e:
            logging.error(e)
            raise e

    def clear(self):
        try:
            self._request_handler.redis.delete("sess_%s" % self.session_id)
        except Exception as e:
            logging.error(e)
        self._request_handler.clear_cookie("session_id")



"""
class xxxxhandler(RequestHandler):
    def post(self):

        session = Session(self)
        session.session_id
        session.data["username"] = "abc"
        session.data["mobile"] = "abc"
        session.save()

    def get(self):
        session = Session(self)
        session.data["username"] = "def"
        session.save()



    def get(self):
        session = Session(self)
        session.clear()

        session.clear()

redis中的数据：
key:    session_id
value:  data
"""
