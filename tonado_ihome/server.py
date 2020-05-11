import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

import config
import urls

tornado.options.define('port',default=8010,type=int,help='run server on the given')

class Application(tornado.web.Application):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

def main():
    '''
    这两行代码要写在tornado.options.parse_command_line()这行代码上面，不然生成不了log文件。原因是tornado.options.parse_command_line() 会将转换后的值对应的设置到全局options对象相关属性上
    如果想将这两行代码写在tornado.options.parse_command_line()下面，设置下tornado.options.define（）就行
    '''
    #日志文件
    tornado.options.options.log_file_prefix=config.log_path
    tornado.options.options.logging = config.log_level

    tornado.options.parse_command_line()  #转换命令行参数，并将转换后的值对应的设置到全局options对象相关属性上

    app=Application(
        urls.urls,
        **config.settings
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)  #tornado.options.options全局的options对象，所有定义的选项变量都会作为该对象的属性。
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()