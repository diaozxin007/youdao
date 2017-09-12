import httplib, urllib

def post(url,parameters):
    params = urllib.urlencode(parameters)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = httplib.HTTPConnection(url)
    conn.request('POST','/api',params,headers)
    response = conn.getresponse()
    return response