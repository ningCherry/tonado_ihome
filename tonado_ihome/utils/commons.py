import functools

from .response_code import RET

# from config import mysql_options
# import pymysql

def required_login(func):
    # 保证被装饰的函数对象的__name__不变
    @functools.wraps(func)
    def wrapper(request_handler_obj,*args,**kwargs):
        # 调用get_current_user方法判断用户是否登录
        if not request_handler_obj.get_current_user():
            request_handler_obj.write(dict(errcode=RET.SESSIONERR, errmsg="用户未登录"))
        else:
            func(request_handler_obj,*args,**kwargs)
    return wrapper


# def mysql_db():
#     db=pymysql.Connect(**mysql_options)
#     cursor=db.cursor()
#     return cursor