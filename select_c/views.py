from django.shortcuts import render
from django.shortcuts import redirect
from select_c import models
from functools import wraps
loginuser=[]
# Create your views here.
def index(request):
    return render(request, 'index.html')

def gochange(request):
    if request.method == 'POST':
        return render(request, 'changepass.html')

def login(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if username=="991104" and password == "990123":
                loginuser.clear()
                return render(request,'index.html')
            try:
                data_pass = models.user.objects.get(userid=username).password #select password  from user where userid=username
                if password == data_pass:
                    if username in loginuser:
                        return render(request,'index.html',{'data':"账号已经登陆，请勿重复登录！"})
                    loginuser.append(username)
                    print(loginuser)
                    request.session["is_login"] = True
                    request.session["name"] = username
                    if len(username) == 8:
                        # request.session.set_expiry[10000]
                        sname=models.S.objects.get(sid=username).sname #select sname from S where sid = username
                        sex = models.S.objects.get(sid=username).sex    #select sex from S where sid = username
                        academy = models.S.objects.get(sid=username).academy    #select academy from S where sid = username
                        age = models.S.objects.get(sid=username).age    #select age from S where sid = username
                        temp = {'username': request.session.get("name"), 'sname': sname,'sex':sex,'academy':academy,'age':age}
                        course_table = models.O.objects.all()      #select * from O
                        select_table = models.E.objects.filter(sid=username)    #slect * from E where sid=username
                        return render(request, 'login.html', {'data': temp,'table':course_table,'table_s':select_table})
                    elif len(username) == 5:
                        tname = models.T.objects.get(tid=username).tname    #select tname from T where tid=username
                        sex = models.T.objects.get(tid=username).sex    #select sex from T where tid=username
                        academy = models.T.objects.get(tid=username).academy    #select academy from T where tid=username
                        age = models.T.objects.get(tid=username).age    #select age from T where tid=username
                        temp = {'username': request.session.get("name"), 'tname': tname, 'sex': sex, 'academy': academy,
                                'age': age}
                        course_table = models.O.objects.filter(tid=username)    #select * from O
                        return render(request, 'login_fort.html', {'data': temp, 'table': course_table})
                else:
                    return render(request, 'index.html',{'data':"密码错误，登陆失败"})
            except:
                return render(request, 'index.html',{'data':"不存在用户"})
        elif 'changepassword' in request.POST:
            return render(request, 'changepass.html')


def changepass(request):
        try:
            if request.method == 'POST':
                username = request.POST.get('username', None)
                oldpassword = request.POST.get('oldpassword',None)
                password = request.POST.get('password', None)
                ack_password = request.POST.get('ack_password',None)
                data_pass = models.user.objects.get(userid=username).password   #select password from user where userid=username
                if oldpassword == data_pass and ack_password == password:
                    models.user.objects.filter(userid=username).update(password=password)   #update user set password=password where userid=username
                    return render(request, 'index.html', {'data': "修改密码成功，请重新登陆"})
                else:
                    return render(request,'changepass.html',{'data':"输入的密码不正确，请重新输入"})
            else:
                return render(request, 'changepass.html')
        except:
            return render(request, 'changepass.html',{'data':"用户不存在"})

def check_login(func):
    @wraps(func)  # 装饰器修复技术
    def inner(request, *args, **kwargs):
        ret = request.session.get("is_login")
        # 1. 获取cookie中的随机字符串
        # 2. 根据随机字符串去数据库取 session_data --> 解密 --> 反序列化成字典
        # 3. 在字典里面 根据 is_login 取具体的数据

        if ret == "1":
            # 已经登录，继续执行
            return func(request, *args, **kwargs)
        # 没有登录过
        else:
            # ** 即使登录成功也只能跳转到home页面，现在通过在URL中加上next指定跳转的页面
            # 获取当前访问的URL
            next_url = request.path_info
            return redirect("/login/?next={}".format(next_url))
    return inner


def submit(request):
    if request.method == 'POST':
        if request.session["is_login"] == True:
            cid = request.POST.get('cno', None)
            tid = models.O.objects.get(cid=cid).tid #select tid from O where cid=cid
            username=request.session.get("name")
            sname = models.S.objects.get(sid=username).sname    #select sname from S where sid=username
            sex = models.S.objects.get(sid=username).sex     #select sex from S where sid=username
            academy = models.S.objects.get(sid=username).academy     #select academy from S where sid=username
            age = models.S.objects.get(sid=username).age     #select age from S where sid=username
            cname=models.O.objects.get(cid=cid).cname    #select cname from O where cid=cid
            tname=models.O.objects.get(cid=cid).tname   #select tname from O where cid=cid
            course_table = models.O.objects.all()       #select * from O
            if 'choose' in request.POST:
                try:
                    test=models.E.objects.get(sid=username,cid=cid,tid=tid) #select * from E where sid=username and cid=cid and tid=tid
                    flag = "已选课程，选课失败"
                    temp = {'username': request.session.get("name"), 'sname': sname, 'sex': sex, 'academy': academy,
                            'age': age, 'flag': flag}
                except:
                    models.E.objects.create(sid=username,sname=sname,cname=cname,tname=tname, cid=cid, tid=tid, kscj=0, pscj=0, zpcj=0)
                    flag = "选课成功"   #insert into E values(username,sname,cname,tname,cid,tid,0,0,0)
                    temp = {'username': request.session.get("name"), 'sname': sname, 'sex': sex, 'academy': academy,
                            'age': age, 'flag': flag}
            if 'quit' in request.POST:
                try:
                    test = models.E.objects.get(sid=username, cid=cid, tid=tid) #select * from E where sid=username and cid=cid and tid=tid
                    models.E.objects.filter(sid=username, cid=cid, tid=tid).delete()    #delete from E where sid=username and cid=cid and tid=tid
                    flag = "退课成功"
                    temp = {'username': request.session.get("name"), 'sname': sname, 'sex': sex, 'academy': academy,
                            'age': age, 'flag': flag}
                except:
                    flag = "没选课程，退课失败"
                    temp = {'username': request.session.get("name"), 'sname': sname, 'sex': sex, 'academy': academy,
                            'age': age, 'flag': flag}
            select_table = models.E.objects.filter(sid=username)    #select * from E where sid=username
            return render(request, 'login.html', {'data': temp, 'table': course_table,'table_s':select_table})


def managec(request):
    if request.session["is_login"] == True:
        if 'managec' in request.POST:
            username = request.session.get("name")
            tname = models.T.objects.get(tid=username).tname    #select tname from T where tid=username
            sex = models.T.objects.get(tid=username).sex    #select sex from T where tid=usrname
            academy = models.T.objects.get(tid=username).academy     #select academy from T where tid=usrname
            age = models.T.objects.get(tid=username).age     #select age from T where tid=usrname
            temp = {'username': request.session.get("name"), 'tname': tname, 'sex': sex, 'academy': academy,
                    'age': age}
            cid = request.POST.get('cno', None)
            table_e=models.E.objects.filter(cid=cid,tid=request.session.get("name"))    #select * from E where cid=cid and tid=tid
            return render(request,'managec.html',{'data':temp ,'table_e':table_e})




def changegrade(request):
    if request.session["is_login"] == True:
        username = request.session.get("name")
        tname = models.T.objects.get(tid=username).tname     #select tname from T where tid=usrname
        sex = models.T.objects.get(tid=username).sex     #select sex from T where tid=usrname
        academy = models.T.objects.get(tid=username).academy     #select academy from T where tid=usrname
        age = models.T.objects.get(tid=username).age     #select age from T where tid=usrname
        temp = {'username': request.session.get("name"), 'tname': tname, 'sex': sex, 'academy': academy,
                'age': age}
        sid=request.POST.get('sid',None)
        cid=request.POST.get('cid',None)
        tid=request.POST.get('tid',None)
        kind=request.POST.get('kind',None)
        newcj=request.POST.get('newcj',None)
        newcj=float(newcj)
        if newcj>100 or newcj<0:
            table_e = models.E.objects.filter(cid=cid, tid=tid)  #select * from E where tid=tid and cid=cid
            return render(request,'managec.html',{'data':temp,'table_e':table_e,'flag':"请输入0-100之间的成绩数据"})
        if kind == 'pscj':
            models.E.objects.filter(sid=sid,cid=cid,tid=tid).update(pscj=newcj) #update E set pscj=newcj where sid=sid and cid=cid and tid=tid
        elif kind == 'kscj':
            models.E.objects.filter(sid=sid,cid=cid,tid=tid).update(kscj=newcj) #update E set kscj=newcj where sid=sid and cid=cid and tid=tid
        pscj=models.E.objects.get(sid=sid,cid=cid,tid=tid).pscj #select pscj from E where sid=sid and cid=cid and tid=tid
        kscj=models.E.objects.get(sid=sid,cid=cid,tid=tid).kscj #select kscj from E where sid=sid and cid=cid and tid=tid
        test=models.O.objects.get(cid=cid).test #select test from O where cid=cid
        normal=models.O.objects.get(cid=cid).normal
        zpcj=pscj*(normal/10)+kscj*(test/10)
        print(zpcj)
        models.E.objects.filter(sid=sid, cid=cid, tid=tid).update(zpcj=zpcj) #update E set zpcj=zpcj where cid=cid and sid=sid and tid=tid
        table_e = models.E.objects.filter(cid=cid, tid=tid) #select * from E where cid=cid and tid=tid
        return render(request,'managec.html',{'data':temp,'table_e':table_e ,'flag':"修改成功"})

def opencrouse(request):
    if request.session["is_login"] == True:
        tid=request.session.get("name")
        tname = models.T.objects.get(tid=tid).tname #select tname from T where tid=tid
        sex = models.T.objects.get(tid=tid).sex #select sex from T where tid=tid
        academy = models.T.objects.get(tid=tid).academy #select academy from T where tid=tid
        age = models.T.objects.get(tid=tid).age #select age from T where tid=tid
        temp = {'username': request.session.get("name"), 'tname': tname, 'sex': sex, 'academy': academy,
                'age': age}
        cid=request.POST.get('cid',None)
        if models.O.objects.filter(cid=cid).count():    #select count(cid=cid) from O
            course_table = models.O.objects.filter(tid=tid) #select * from O where tid=tid
            return render(request,'login_fort.html', {'data': temp, 'table': course_table,'flag':"课号已存在，请更换课号"})
        cname=request.POST.get('cname',None)
        academy=request.POST.get('academy',None)
        credit=request.POST.get('credit',None)
        test=request.POST.get('test',None)
        normal=request.POST.get('normal',None)
        credit=float(credit)
        test=float(test)
        normal=float(normal)
        if test+normal != 10:
            course_table = models.O.objects.filter(tid=tid) #select * from O where tid=tid
            return render(request, 'login_fort.html', {'data': temp, 'table': course_table, 'flag': "平时占比和考试占比和不为10，请重新输入"})
        models.O.objects.create(cid=cid,cname=cname,academy=academy,tname=tname,tid=tid,credit=credit,test=test,normal=normal)
        #insert into O values(cname,academy,tname,tid,credit,test,normal)
        course_table = models.O.objects.filter(tid=tid) #select * from O where tid=tid
        return render(request, 'login_fort.html', {'data': temp, 'table': course_table,'flag':"开课成功"})



def quit(request):
    if request.session["is_login"]==True:
        request.session["is_login"] = False
        username = request.session.get("name")
        loginuser.remove(username)
        return render(request, 'index.html')


def back(request):
    if request.session["is_login"] == True:
        username = request.session.get("name")
        tname = models.T.objects.get(tid=username).tname  # select tname from T where tid=username
        sex = models.T.objects.get(tid=username).sex  # select sex from T where tid=username
        academy = models.T.objects.get(tid=username).academy  # select academy from T where tid=username
        age = models.T.objects.get(tid=username).age  # selcet age from T where tid=username
        temp = {'username': request.session.get("name"), 'tname': tname, 'sex': sex, 'academy': academy,
                'age': age}
        course_table = models.O.objects.filter(tid=username)  # selcet * from O where tid=username
        return render(request, 'login_fort.html', {'data': temp, 'table': course_table})