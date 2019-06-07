# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.request import CommonRequest
# import random


# def sendMessage(req,number):
#     number = number
#     client = AcsClient('LTAI440I6g1z8s7u', '5WKvQX7CitmnCFTWCDIbSWbycxd5wo', 'default')

#     request = CommonRequest()
#     request.set_accept_format('json')
#     request.set_domain('dysmsapi.aliyuncs.com')
#     request.set_method('POST')
#     request.set_protocol_type('https')
#     request.set_version('2017-05-25')
#     request.set_action_name('SendSms')

#     code = ''
#     for i in range(0,6):
#         code = code + str(random.randint(0, 9))

#     request.add_query_param('PhoneNumbers', '%s'%number)
#     request.add_query_param('SignName', 'TopChat')
#     if req == 'regist':
#         request.add_query_param('TemplateCode', 'SMS_160306084')
#     elif req == 'phonenumber':
#         request.add_query_param('TemplateCode', 'SMS_160306090')
#     elif req == 'password':
#         request.add_query_param('TemplateCode', 'SMS_160306088')
#     request.add_query_param('TemplateParam', '{"code":"%s","product":"ytx"}'%code)

#     response = client.do_action(request)
#     # python2:  print(response) 
#     # print(str(response, encoding = 'utf-8'))
#     return code



import zhenzismsclient as smsclient
import random
client = smsclient.ZhenziSmsClient('https://sms_developer.zhenzikj.com',
'100991','ODFhYzAxNWYtMGYzMS00Yjk5LWE5MmEtY2Y2MDY5YTQyMTFm')



def sendMessage(req,number):
    code = ''
    for num in range(0,6):
        code = code + str(random.randint(0, 9))
    if req == 'regist':
        result = client.send(number, '您正在注册TopChat,验证码为：'+code)
    elif req == 'phonenumber':
        result = client.send(number,'您正在修改绑定手机号,验证码为：'+code)
    elif req == 'password':
        result = client.send(number,'您正在修改密码,验证码为：'+code)

    return code