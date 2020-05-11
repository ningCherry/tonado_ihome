from .BaseHandler import BaseHandler
import logging
import io
import re
import random

from utils.captcha.captcha import create_validate_code
from constants import *
from utils.response_code import RET
from utils.yuntongxun.SendTemplateSMS import ccp


class PicCodeHandler(BaseHandler):
    # #验证图形验证码
    # def get(self, *args, **kwargs):
    #     # 创建一个文件流
    #     imgio = io.BytesIO()
    #     # 生成图片对象和对应字符串
    #     img, code = create_validate_code()
    #     # 将图片信息保存到文件流
    #     img.save(imgio, 'GIF')
    #     # 返回图片
    #     self.set_header("Content-Type", "image/jpg")
    #     self.write(imgio.getvalue())


    """图片验证码"""
    def get(self):
        """获取图片验证码"""
        pre_code_id = self.get_argument("pre", "")
        cur_code_id = self.get_argument("cur","")
        # 创建一个文件流
        imgio = io.BytesIO()
        # 生成图片对象和对应字符串
        pic, text= create_validate_code()
        # 将图片信息保存到文件流
        pic.save(imgio, 'GIF')

        try:
            if pre_code_id:
                self.redis.delete("pic_code_%s" % pre_code_id)
                # self.redis.delete("")
            # self.redis.setex(name, expries, value)
            self.redis.setex("pic_code_%s" % cur_code_id, PIC_CODE_EXPIRES_SECONDS, text)
        except Exception as e:
            logging.error(e)
            self.write("")
        else:
            self.set_header("Content-Type", "image/jpg")
            # 返回图片
            self.write(imgio.getvalue())


"""短信验证码"""
class SMSCodeHandler(BaseHandler):
    def post(self):
        mobile=self.json_args.get("mobile")
        piccode=self.json_args.get("piccode")
        piccode_id=self.json_args.get("piccode_id")
        print(mobile,piccode,piccode_id)

        # 参数校验
        if not all((mobile,piccode,piccode_id)):
            return self.write(dict(errcode=RET.PARAMERR,errmsg='参数缺失'))
        if not re.match(r'^1\d{10}$',mobile):
            return self.write(dict(errcode=RET.PARAMERR,errmsg='手机号格式错误'))

        # 获取图片验证码真实值
        global real_piccode
        if piccode!='1234':    #设置万能图形验证码
            try:
                real_piccode = self.redis.get("pic_code_%s" % piccode_id)
            except Exception as e:
                logging.error(e)
                self.write(dict(errcode=RET.DBERR, errmsg='查询验证码错误'))
            if not real_piccode:  # real_piccode要定义为全局变量，不然会报错
                return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))

            # 判断图形验证码正确性
            if real_piccode.decode('utf-8').lower() != piccode.lower():  ##redis数据real_piccode要解码
                # print(real_piccode.lower())
                # print(piccode.lower())
                return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))

        #检查手机号码是否存在
        # sql = "select count(*) counts from ih_user_profile where up_mobile=%s"
        # try:
        #     ret = self.db.get(sql, mobile)
        # except Exception as e:
        #     logging.error(e)
        # else:
        #     if 0 != ret["counts"]:
        #         return self.write(dict(errcode=RET.DATAEXIST, errmsg="手机号已注册"))

        #生成随机短信验证码
        sms_code="%04d" %random.randint(0,9999)
        try:
            self.redis.setex("sms_code_%s" % mobile, SMS_CODE_EXPIRES_SECONDS, sms_code)
        except Exception as e:
            logging.error(e)
            self.write(dict(errcode=RET.DBERR, errmsg='数据库出错'))

        #发送短信验证码
        global result
        try:
            result=ccp.sendTemplateSMS(mobile,[sms_code,SMS_CODE_EXPIRES_SECONDS/60],1)
        except Exception as e:
            logging.error(e)
            self.write(dict(errcode=RET.THIRDERR, errmsg='发送短信失败'))
        if result:
            self.write(dict(errcode=RET.OK, errmsg='发送成功'))
        else:
            self.write(dict(errcode=RET.UNKOWNERR, errmsg='发送失败'))



