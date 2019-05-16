import tornado
import os
from tornado import web, ioloop, httpserver
import requests,re
import pymysql
import requests,time
from urllib import parse

xuexin_headers = {
"Host": "account.chsi.com.cn",
"Connection": "keep-alive",
"Content-Length": "56",
"Accept": "application/json, text/javascript, */*; q=0.01",
"Origin": "https://account.chsi.com.cn",
"X-Requested-With": "XMLHttpRequest",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"Referer": "https://account.chsi.com.cn/account/preregister.action?from=archive",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cookie": "JSESSIONID=846A5C43BDB726231FDF897A14D88F72; Secure; __utma=65168252.980312581.1526972694.1526972694.1526972694.1; __utmz=65168252.1526972694.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.3.980312581.1526972694; __utma=39553075.980312581.1526972694.1526972722.1526972722.1; __utmz=39553075.1526972722.1.1.utmcsr=my.chsi.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/archive/index.jsp",
}
def xuexin_check_number(number):
    if len(number)!=11:
        print(number, "---- 位数不足")
    else:
        url = "https://account.chsi.com.cn/account/checkmobilephoneother.action"
        form_data = [('mphone', number),
                     ('dataInfo', number),
                     ('optType', 'REGISTER'),
                     ]
        page = requests.post(url, headers=xuexin_headers, data=form_data).text
        result = re.findall("[a-z]{4,5}",page)
        if result:
            if result[0]=="true":
                print(number,"---- 可以注册")
            elif result[0]=="false":
                print(number, "---- 已经注册")
                # 打开数据库连接
                db = pymysql.connect("localhost", "root", "root", "searchyou")
                # 使用cursor()方法获取操作游标
                cursor = db.cursor()

                # SQL 更新语句
                sql = "UPDATE FLAG SET FLAG = TRUE WHERE ID = 1"
                try:
                    # 执行SQL语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # 发生错误时回滚
                    db.rollback()

                # 关闭数据库连接
                db.close()
        else:
            print(number,"---- 验证失败")
def weibo_check_number(number):
    header = {
        "Host": "weibo.com",
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": "https://weibo.com/signup/signup.php",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "UOR=cuiqingcai.com,widget.weibo.com,cuiqingcai.com; SINAGLOBAL=4488993145257.228.1526896503332; SCF=AlC33K5qfoC7HrROfBB4mJtN4jIrVfmOXc5lAUlmorulSufEgLxzAoaGm9UpO3hHKasTrfkIe_0LeF5Zd8gRv7M.; SUHB=0nlfv7xtsoHJQt; YF-Ugrow-G0=ad83bc19c1269e709f753b172bddb094; SUB=_2AkMsSHHIf8NxqwJRmP4RzmvkaY9_yQ_EieKaFIATJRMxHRl-yT83qkYgtRB6B8hfJraHaIVDNybz4ulKcpL4rU8_KteM; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFzw.rJdFEwdBoiQG9_E9Hi; login_sid_t=c8537f18996d44a673568d321f8c5072; cross_origin_proto=SSL; YF-V5-G0=16139189c1dbd74e7d073bc6ebfa4935; WBStorage=5548c0baa42e6f3d|undefined; _s_tentry=passport.weibo.com; wb_view_log=1366*7681; __lnkrntdmcvrd=-1; Apache=6358580283442.719.1528102658639; ULV=1528102658655:2:1:1:6358580283442.719.1528102658639:1526896504059; appkey=",
    }
    url = "https://weibo.com/signup/v5/formcheck?type=mobilesea&zone=0086&value="+number+"&from=&__rnd=" + str(
        int(time.time()) * 13)
    res = requests.get(url, headers=header).text
    res = parse.unquote(res)
    print(res.encode('utf-8').decode('unicode_escape')[9:15])
    weibo_flag = res.encode('utf-8').decode('unicode_escape')[9:15]
    if weibo_flag == "100000":
        print(number, "---- 可以注册")
    elif weibo_flag == "600001":
        print(number, "---- 已经注册")
        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "root", "searchyou")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 更新语句
        sql = "UPDATE FLAG SET FLAG = TRUE WHERE ID = 2"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

        # 关闭数据库连接
        db.close()
    else:
        print(number,"---- 验证失败")

#业务模块 部门
class MainPageHandler(web.RequestHandler):
    def get(self,*args,**kwargs):
       # self.write(' 学习是积累的事情，一口吃不成一个胖子')
        self.render('index.html')
    def post(self,*args,**kwargs):
        pass

#创建游戏
class CreateGameHandler(web.RequestHandler):
    def post(self,*args,**kwargs):
        #接收 前台传过来的数据
        telphone = self.get_argument('telphone')
        print(telphone)
        weibo_check_number(telphone)
        xuexin_check_number(telphone)

        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "root", "searchyou")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 更新语句
        sql = "SELECT NAME,FLAG FROM FLAG WHERE FLAG = 1 "
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                name = row[0]
                flag = row[1]
                # 打印结果
                print(name,flag)
        except:
            print
            "Error: unable to fecth data"

        # 关闭数据库连接
        db.close()
        self.render('result.html',results=results)


#配置
settings = {
    'template_path':'templates',
    'static_path':'static'
}

#路由系统
application = web.Application([
    (r"/", MainPageHandler),
    (r"/create_game", CreateGameHandler),
],**settings)

if __name__ == '__main__':
    print(os.listdir())
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8080)
    ioloop.IOLoop.current().start()
