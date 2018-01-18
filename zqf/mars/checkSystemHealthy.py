#-*- coding:utf-8 -*-
'''
Team     : Core Service Regional Application Team
Module   : Base functions of monitoring
Purpose  ：Monitoring Service Healthy & Collect sys availability data
Desc     : ping p_host, check service port, simulate user logon action
           to verify the availability of service. and with those data,
           service availability can be count during specified period.
------- -------- ------------ ----------------------------------
Ver     CCYYMMDD Modified     Desc
------- -------- ------------ ----------------------------------
V1.0    20180111 Carlo Zhang  Initial Version
------- -------- ------------ ----------------------------------
'''
import os
import socket
import datetime
import subprocess
import traceback
import platform
import urllib
import urllib2
import sys
from saveLog2SQLite import save_monitor_log_db
'''
Func: pingServer
Desc: Ping Server
'''
def pingServer(p_host,p_desc):
    job_time=(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    if platform.system()=='Windows':
        cmd = 'ping -n %d %s'%(1,p_host)
    else:
        cmd = 'ping -c %d %s'%(1,p_host)
    try:
        p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (stdoutput,erroutput) = p.communicate()
        #print stdoutput
    except Exception, e:
        #traceback.print_exc()
        pass
    result_flag = 'failed'
    if platform.system()=='Windows' and stdoutput.find('Received = 1')>=0:
        print '%-50s|%-5s |ok  |%-19s|%s' % (p_host,"ping",job_time,p_desc)
        result_flag = 'succeed'
    elif platform.system()=='Windows' and stdoutput.find('Received = 1')<0:
        print '%-50s|%-5s |fail|%-19s|%s' % (p_host,"ping",job_time,p_desc)
    else:
        print stdoutput.find('1 packets received')>=0
        
    save_monitor_log_db([(
                          p_host,'Ping Host',\
                          result_flag, \
                          job_time, \
                          p_desc.decode('utf-8'),\
                          ''\
                          )])
'''
Func: chkSvrPort
Desc: Connect to specified port of server to check the accessability
'''
def chkSvrPort(p_host,p_port,p_desc):
    job_time=(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((p_host,int(p_port)))
        s.shutdown(2)
        print '%-50s|%-5s |ok  |%-19s|%s' % (p_host,p_port,job_time,p_desc)
        result_flag = 'succeed'
    except:
        print '%-50s|%-5s |fail|%-19s|%s' % (p_host,p_port,job_time,p_desc)
        result_flag = 'failed'
    save_monitor_log_db([(
                          p_host,p_port,\
                          result_flag, \
                          job_time, \
                          p_desc.decode('utf-8'),\
                          ''\
                          )])
'''
Func: stmlSysAct
Desc: Simulate user login action to check if sys can be logon successfully
'''
def stmlSysAct(p_url,p_parm,p_success_flag,p_desc):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    job_time=(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    flag_validation = False
    req_parm = p_parm
    req_url = p_url
    login_ok_flag = p_success_flag
	
    req_parm_urlencode = urllib.urlencode(req_parm)
    req = urllib2.Request(url = req_url,data =req_parm_urlencode)
    try:
        rps_data = urllib2.urlopen(req)
        rps_html = rps_data.read().decode('utf-8')
        if login_ok_flag in rps_html:
            flag_validation = True
    except Exception, e:
        pass
    if flag_validation == True:
        print '%-50s|login |ok  |%-19s|(%s)' % (p_url,job_time,p_desc.decode('utf-8'))
        result_flag = 'succeed'
    else:
        print '%-50s|login |fail|%-19s|(%s)' % (p_url,job_time,p_desc.decode('utf-8'))
        result_flag = 'failed'
    save_monitor_log_db([(
                          p_url,\
                          'Simulate URL Login',\
                          result_flag, \
                          job_time, \
                          p_desc.decode('utf-8'), \
                          req_parm_urlencode\
                          )])
'''
待添加:
1） 检查自己给出去的接口
    Web Service
    DB 数据表是否有数据
    指定目录文件是否生成
2） 检查上游提供的接口（同上）
3） 检查当天DB Job完成情况
4） 每10分钟检查异常数据（VNM Replenishment）
'''

'''
Example
'''
if __name__ == '__1main__':
    
    
    data = stmlSysAct_test(p_url = "http://urlurl:9010/wrigley/login.do", \
               p_parm = {'userAccount':'cszhangca21','userPassword':'carlo12345'},\
               p_success_flag = "欢迎登录", \
               p_desc = '测试错误URL，登录失败')
               
    data = data + stmlSysAct_test(p_url = "http://efexap.effem.com.cn:9010/wrigley/login.do", \
               p_parm = {'userAccount':'cszhangca2','userPassword':'carlo12345'},\
               p_success_flag = "欢迎登录",\
               p_desc = '测试成功登录')
    data = data + stmlSysAct_test(p_url = "http://efexap.effem.com.cn:9010/wrigley/login.do", \
               p_parm = {'userAccount':'error','userPassword':'carlo12345'},\
               p_success_flag = "欢迎登录",\
               p_desc = '测试错误帐号，登陆失败')
               
    save_monitor_log_db(data)
    
if __name__ == '__main__':
    
    pingServer('gnzlx005.gnz.ap.mars',     'prd cot db txn svr')
    pingServer('gnzlx006.gnz.ap.mars',     'prd cot db rpt svr')
    pingServer('gnzlx004.gnz.ap.mars',     'prd cot app/img svr')
    pingServer('gnzlx003.gnz.ap.mars',     'prd cot web svr')
    pingServer('gnzlx001.gnz.ap.mars',     'prd efexcn choc web')
    pingServer('isclx003.isc.ap.mars',     'prd efexcn choc db svr')
    pingServer('cngufwerap01.mars-ad.net', 'prd wera lite db svr')
    pingServer('wmap.wrigley.com',         'prd wera lite wwoh & mobility web')
    pingServer('apxg.wrigley.com',         'prd wera lite mobility special func(tst)')
    pingServer('AZR-SAW5009',              'tst MWCCN AZURE db txn & rpt')
    pingServer('AZR-SAW5008',              'tst MWCCN AZURE app')
    pingServer('AZR-SAW5010',              'tst MWCCN AZURE web')
    pingServer('AZR-SAW5011',              'prd MWCCN AZURE db txn')
    pingServer('AZR-SAW5013',              'prd MWCCN AZURE db rpt')
    pingServer('AZR-SAW5014',              'prd MWCCN AZURE app')
    pingServer('AZR-SAW5012',              'prd MWCCN AZURE web')
    
    #Remote Desktop 3389
    chkSvrPort('AZR-SAW5009',              3389, 'tst MWCCN AZURE db txn & rpt')
    chkSvrPort('AZR-SAW5008',              3389, 'tst MWCCN AZURE app')
    chkSvrPort('AZR-SAW5010',              3389, 'tst MWCCN AZURE web')
    chkSvrPort('AZR-SAW5011',              3389, 'prd MWCCN AZURE db txn')
    chkSvrPort('AZR-SAW5013',              3389, 'prd MWCCN AZURE db rpt')
    chkSvrPort('AZR-SAW5014',              3389, 'prd MWCCN AZURE app')
    chkSvrPort('AZR-SAW5012',              3389, 'prd MWCCN AZURE web')
    
    #COT DB Server
    chkSvrPort('gnzlx005.gnz.ap.mars',     1521, 'prd cot db txn')
    chkSvrPort('gnzlx006.gnz.ap.mars',     1521, 'prd cot db rpt')
    #COT APP Server
    chkSvrPort('gnzlx004.gnz.ap.mars',     8010, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8013, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8014, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8015, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8019, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8021, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8022, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8025, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8026, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8027, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8028, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8029, 'prd cot app/img (MarsAD)')
    chkSvrPort('gnzlx004.gnz.ap.mars',     8030, 'prd cot app/img (MarsAD)')
    chkSvrPort('cot.wrigley.com',          8010, 'prd cot app/img (Internal DNS)')
    #COT Web Server
    chkSvrPort('gnzlx003.gnz.ap.mars',     8001, 'prd cot web (MarsAD) portal')
    chkSvrPort('gnzlx003.gnz.ap.mars',     8002, 'prd cot web (MarsAD)')
    chkSvrPort('gnzlx003.gnz.ap.mars',     8003, 'prd cot web (MarsAD)')
    chkSvrPort('gnzlx003.gnz.ap.mars',     8004, 'prd cot web (MarsAD)')
    chkSvrPort('gnzlx003.gnz.ap.mars',     8005, 'prd cot web (MarsAD) mobility func')
    chkSvrPort('gnzlx003.gnz.ap.mars',     8006, 'prd cot web (MarsAD) schedule task')
    chkSvrPort('gnzlx003.gnz.ap.mars',     8007, 'prd cot web (MarsAD)')
    chkSvrPort('14.23.90.135',             8001, 'prd cot web (efex.wrigley.com.cn) portal')
    chkSvrPort('14.23.90.135',             8002, 'prd cot web (efex.wrigley.com.cn)')
    chkSvrPort('14.23.90.135',             8003, 'prd cot web (efex.wrigley.com.cn)')
    chkSvrPort('14.23.90.135',             8004, 'prd cot web (efex.wrigley.com.cn)')
    chkSvrPort('14.23.90.135',             8005, 'prd cot web (efex.wrigley.com.cn) mobility func')
    chkSvrPort('14.23.90.135',             8006, 'prd cot web (efex.wrigley.com.cn) schedule task')
    chkSvrPort('14.23.90.135',             8007, 'prd cot web (efex.wrigley.com.cn)')
    #EFEXCN & RTMCN Web Server
    chkSvrPort('gnzlx001.gnz.ap.mars',     80,   'prd efexcn choc web portal(MarsAD)')
    chkSvrPort('gnzlx001.gnz.ap.mars',     9100, 'prd efexcn choc web rtm portal(MarsAD)')
    chkSvrPort('gnzlx001.gnz.ap.mars',     9041, 'prd efexcn choc web mobility func(MarsAD)')
    chkSvrPort('gnzlx001.gnz.ap.mars',     9042, 'prd efexcn choc web schedule task(MarsAD)')
    chkSvrPort('efexv2.effem.com.cn',      80,   'prd efexcn choc web portal(PublicURL)')
    chkSvrPort('efexv2.effem.com.cn',      9100, 'prd efexcn choc web rtm portal(PublicURL)')
    chkSvrPort('efexv2.effem.com.cn',      9041, 'prd efexcn choc web mobility func(PublicURL)')
    chkSvrPort('efexv2.effem.com.cn',      9042, 'prd efexcn choc web schedule task(PublicURL)')
    #EFEXCN & RTMCN & EFEXAP TXN DB Server
    chkSvrPort('isclx003.isc.ap.mars',     1521, 'prd efexcn & rtmcn db txn')
    #WERA LITE DB Server
    chkSvrPort('cngufwerap01.mars-ad.net', 1521, 'prd wera lite db')
    chkSvrPort('wmap.wrigley.com',         80,   'prd wera lite wwoh & mobility web(MarsAD)')    
    chkSvrPort('apxg.wrigley.com',         443,  'prd wera lite mobility special func(MarsAD)')
    chkSvrPort('14.23.90.138',             80,   'prd wera lite wwoh & mobility web (PublicIP)')    
    chkSvrPort('59.37.4.103',              443,  'prd wera lite mobility special func(tst)(PublicIP)')
    #MWCCN Azure Cloud Server
    chkSvrPort('AZR-SAW5009'  ,            10368,'tst mwccn_efex db txn AZR-SAW5009\MI0368T')
    chkSvrPort('AZR-SAW5009'  ,            10374,'tst mwccn_efex db rpt AZR-SAW5009\MI0374T')
    #chkSvrPort('AZR-SAW5008'  ,            80,   'tst mwccn_efex app')
    #chkSvrPort('AZR-SAW5010'  ,            443,  'tst mwccn_efex web(internal ip)')
    chkSvrPort('AZR-SAW5011'  ,            10369,'prd mwccn_efex db txn - AZR-SAW5011\MI0369P')
    chkSvrPort('AZR-SAW5013'  ,            10370,'prd mwccn_efex db rpt - AZR-SAW5013\MI0370P')
    #chkSvrPort('AZR-SAW5014'  ,            80,   'prd mwccn_efex app')
    #chkSvrPort('AZR-SAW5012'  ,            443,  'prd mwccn_efex web(internal ip)')
    #chkSvrPort('52.230.86.65' ,            443,  'prd mwccn_efex web(Public IP1)')
    #chkSvrPort('52.187.121.72',            443,  'prd mwccn_efex web(Public IP1)')

    stmlSysAct(p_url = "http://urlurl:9010/wrigley/login.do", \
               p_parm = {'userAccount':'cszhangca21','userPassword':'carlo12345'},\
               p_success_flag = "欢迎登录", \
               p_desc = '测试错误URL，登录失败')
    stmlSysAct(p_url = "http://efexap.effem.com.cn:9010/wrigley/login.do", \
               p_parm = {'userAccount':'cszhangca2','userPassword':'carlo12345'},\
               p_success_flag = "欢迎登录",\
               p_desc = '测试成功登录')
    stmlSysAct(p_url = "http://efexap.effem.com.cn:9010/wrigley/login.do", \
               p_parm = {'userAccount':'error','userPassword':'carlo12345'},\
               p_success_flag = "欢迎登录",\
               p_desc = '测试错误帐号，登陆失败')