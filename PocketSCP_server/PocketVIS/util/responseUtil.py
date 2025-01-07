# 将请求结果参数进行解析
# demo=demo&test=test&a=2
# {"demo":"demo","test":"test","a":"2"}

def process_request_params(params):
    response_param = {}
    # 分割&
    param = str(params).split("&")
    for data in param:
        p = data.split("=")
        response_param[p[0]] = p[1]
    return response_param
