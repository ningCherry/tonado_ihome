from CCPRestSDK import REST

# import ConfigParser

# 主帐号
accountSid = '8aaf07087162cd7801716e66916f032d'

# 主帐号Token
accountToken = '9d1f68a431f14f1998dd62beb0e492d2'

# 应用Id
appId = '8aaf07087162cd7801716e6691d80334'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

class CCP(object):
    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @staticmethod
    def instance():
        if not hasattr(CCP, "_instance"):
            CCP._instance = CCP()
        return CCP._instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to, datas, tempId)
        except Exception as e:
            # logging.error(e)
            raise e
        # print result
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        success = "<statusCode>000000</statusCode>"
        if success in result:
            return True
        else:
            return False

ccp = CCP.instance()

if __name__ == "__main__":
    ccp = CCP.instance()
    # 1代表模板ID，下载SDK的官网api文档有说明
    ret = ccp.sendTemplateSMS("15801801915", ["aaaa", "1"], 1)

    print(ret)