import requests,re,time
from urllib import parse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib3
import json

req = requests.Session()

class Login(object):
    '''登录'''
    def __init__(self):
        self.username = username
        self.password = password
        self.url_pic = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.15905700266966694'
        self.url_check = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.url_login = 'https://kyfw.12306.cn/passport/web/login'
        self.url_rail_deviceid = 'https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=ePDrudm04F&hashCode=LsiGTHjzxZP4Y0CqYMSqB_gCYSxedrZtc-b-Udn5U64&FMQw=1&q4f3=zh-CN&VySQ=FGE5ZXJgSTAVsIIM9ospTQfYHncbH5Ig&VPIf=1&custID=133&VEek=unknown&dzuS=29.0%20r0&yD16=0&EOQP=f57fa883099df9e46e7ee35d22644d2b&jp76=7047dfdd1d9629c1fb64ef50f95be7ab&hAqN=Win32&platform=WEB&ks0Q=6f0fab7b40ee4a476b4b3ade06fe9065&TeRS=1080x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%206.1;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/63.0.3239.132%20Safari/537.36&E3gR=fd7a8adb89dd5bf3a55038ad1adc5d35&timestamp='
        self.headers={
            'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

    def get_rail_deviceid(self):
        global req
        html_rail_deviceid = req.get(self.url_rail_deviceid+ str(int(time.time()*1000)),headers=self.headers).text
        rail_deviceid = re.search(r'"dfp":"(.*?)"', html_rail_deviceid).group(1)
        req.cookies['RAIL_DEVICEID'] = rail_deviceid

    def showimg(self):
        '''显示验证码图片'''
        global req
        html_pic = req.get(self.url_pic, headers=self.headers).content
        open('pic.jpg', 'wb').write(html_pic)
        img = mpimg.imread('pic.jpg')
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    
    def captcha(self, answer_num):
        '''填写验证码'''
        answer_sp = answer_num.split(',')
        answer_list = []
        an = {'1': (31, 35), '2': (116, 46), '3': (191, 24), '4': (243, 50), '5': (22, 114), '6': (117, 94),
              '7': (167, 120), '8': (251, 105)}
        for i in answer_sp:
            for j in an.keys():
                if i == j:
                    answer_list.append(an[j][0])
                    answer_list.append(',')
                    answer_list.append(an[j][1])
                    answer_list.append(',')
        s = ''
        for i in answer_list:
            s += str(i)
        answer = s[:-1]

        form_check = {
            'answer': answer,
            'login_site': 'E',
            'rand': 'sjrand',
            '_': str(int(time.time() * 1000))
        }
        global req
        html_check = req.get(self.url_check, params=form_check, headers=self.headers).json()
        print(html_check)
        if html_check['result_code'] == '4':
            print('验证码校验成功!')
        else:
            print('验证码校验失败!')
            exit()

    def login(self,answer_num):
        '''登录账号'''
        answer_sp = answer_num.split(',')
        answer_list = []
        an = {'1': (31, 35), '2': (116, 46), '3': (191, 24), '4': (243, 50), '5': (22, 114), '6': (117, 94),
              '7': (167, 120), '8': (251, 105)}
        for i in answer_sp:
            for j in an.keys():
                if i == j:
                    answer_list.append(an[j][0])
                    answer_list.append(',')
                    answer_list.append(an[j][1])
                    answer_list.append(',')
        s = ''
        for i in answer_list:
            s += str(i)
        answer = s[:-1]
        form_login = {
            'username': self.username,
            'password': self.password,
            'appid': 'otn',
            'answer': answer
        }
        print(form_login)
        global req

        html_login = req.post(self.url_login, data=form_login, headers=self.headers).json()
        print(html_login)
        if html_login['result_code'] == 0:
            print('恭喜您,登录成功!')
            select()
        else:
            print('账号密码错误,登录失败!')
            exit()

class Leftquery(object):
    '''余票查询'''

    def __init__(self):
        self.station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        self.headers = {
            'Host': 'kyfw.12306.cn',
            'If-Modified-Since': '0',
            'Pragma': 'no-cache',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def station_name(self, station):
        '''获取车站简拼'''
        html = requests.get(self.station_url, verify=False).text
        result = html.split('@')[1:]
        dict = {}
        for i in result:
            key = str(i.split('|')[1])
            value = str(i.split('|')[2])
            dict[key] = value
        return dict[station]

    def query(self, from_station, to_station, date):
        '''余票查询'''
        fromstation = self.station_name(from_station)
        tostation = self.station_name(to_station)
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
            date, fromstation, tostation)
        
        try:
            html = requests.get(url, headers=self.headers, verify=False).json()
            result = html['data']['result']
            if result == []:
                print('很抱歉,没有查到符合当前条件的列车!')
                exit()
            else:
                print(date + from_station + '-' + to_station + '查询成功!')
                num = 1 
                for i in result:
                    info = i.split('|')
                    if info[0] != '' and info[0] != 'null':
                        print(str(num) + '.' + info[3] + '车次还有余票:')
                        print('出发时间:' + info[8] + ' 到达时间:' + info[9] + ' 历时多久:' + info[10] + ' ', end='')
                        seat = {21: '高级软卧', 23: '软卧', 26: '无座', 28: '硬卧', 29: '硬座', 30: '二等座', 31: '一等座', 32: '商务座',
                                33: '动卧'}
                        from_station_no = info[16]
                        to_station_no = info[17]
                        for j in seat.keys():
                            if info[j] != '无' and info[j] != '':
                                if info[j] == '有':
                                    print(seat[j] + ':有票 ', end='')
                                else:
                                    print(seat[j] + ':有' + info[j] + '张票 ', end='')
                        print('\n')
                    elif info[1] == '预订':
                        print(str(num) + '.' + info[3] + '车次暂时没有余票')
                    elif info[1] == '列车停运':
                        print(str(num) + '.' + info[3] + '车次列车停运')
                    elif info[1] == '23:00-06:00系统维护时间':
                        print(str(num) + '.' + info[3] + '23:00-06:00系统维护时间')
                    else:
                        print(str(num) + '.' + info[3] + '车次列车运行图调整,暂停发售')
                    num += 1
            return result
        except:
            print('查询信息有误!请重新输入!')
            exit()

def show():
    '''显示余票'''
    from_station = input('请输入您要购票的出发地(例:北京):')
    to_station = input('请输入您要购票的目的地(例:上海):')
    date = input('请输入您要购票的乘车日期(例:2019-06-06):')
    query=Leftquery()
    result = query.query(from_station, to_station, date)

def select():
    '''菜单'''
    print("1.登录  2.查票  3.退出")
    print("*"*69)
    func=input("请输入你要操作的选项:")
    global username,password
    if func=='1':
        username=input("请输入你的12306账号名称:")
        password=input("请输入你的12306账号密码:")
        login=Login()
        login.get_rail_deviceid()
        login.showimg()
        # 填写验证码
        print('  =============================================================== ')
        print('   根据打开的图片识别验证码后手动输入，输入正确验证码对应的位置 ')
        print('     --------------------------------------')
        print('            1  |  2  |  3  |  4 ')
        print('     --------------------------------------')
        print('            5  |  6  |  7  |  8 ')
        print('     --------------------------------------- ')
        print(' =============================================================== ')
        answer_num = input('请填入验证码(序号为1~8,中间以逗号隔开,例:1,2):')
        login.captcha(answer_num)
        login.login(answer_num)
    if func=='2':
        show()
        select()
    if func=='3':
        exit()
    else:
        print("输入有误，请重新输入")
        print("*"*69)
        select()

if __name__ == '__main__':
    print('*' * 30 + '12306' + '*' * 30)
    select() 
