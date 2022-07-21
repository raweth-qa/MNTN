import requests
import json
import unittest
from pprint import pprint
import urllib
import sys
import inspect
import code

'''
This is a very basic set of calls to kick the tires using the https protocol (no one uses http its insecure) .. unfortunatley without a key
  this would normally be wither an auth token in the headers or possibly a jwt token as part of the calls
https://httpbin.org/headers

optimally you would build this off a client class object with member variables instantiated to reflect these
  tokens, with convienance wrapped methods.

This is prototype code
To cut corners this is one big encapsulated file with everything it needs.
In a test framework you should never write code like this you should have a strong
  Frameowrk such as pytest or somthing else (unitest is a bit old)
  Libraries with class and function modules
  test scripts that employ the modules and the test framework
  ideally the test can and should be modified to handle
     a parameter based environment ie  dev qa or staging to run the approiate api calls in that framework
     unittest output or some other agreed format to record reults of the test in jenkins   

'''

#
# very usefull for debugging in shell
#
def bkpoint(msg=""):
    '''Stops execution of code bringing up python console and prints msg'''
    # Use exception trick to pick up the current frame
    try:
        raise None
    except:
        frame = sys.exc_info()[2].tb_frame.f_back

    from inspect import currentframe, getframeinfo
    frameinfo = getframeinfo(currentframe().f_back)

    # Evaluate commands in current namespace
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)
    code.interact(banner="bkpoint %s %s>>" % (frameinfo.filename, frameinfo.lineno), local=namespace)


#
# this is a wrap of the client rest calls
# it has a strong nameing convention:
#   resource_<method post/put/get ..>_addnlPath
# this should be ported to a separate library
#
class BinOrgApi():
    def __init__(self):
        self.host = 'httpbin.org'
        self.server = "https://httpbin.org/"
        self.headers = {'content-type': 'application/json'}
        self.timeout = 30

    #def postRest(self,_url,parm_dict):

    def getRest(self,_url):
        r = requests.get(_url, headers=self.headers, timeout=self.timeout)
        return r


    def postRestQuery(self,_url,payload):
        # this is a very sad form of posting which employs a query string
        # normal posts should have the same _url path and vary in the data supplied
        # sadly this does not
        #params = urlencode(payload, quote_via=quote_plus)
        params= urllib.parse.urlencode(payload)
        _url += f"?freeform={params}"
        #https://httpbin.org/response-headers?freeform=%7B'sheldon_cooper'%3A'bazinga'%7D
        r = requests.post(_url,data=json.dumps(payload),headers=self.headers, timeout=self.timeout)
        return r

    def putRest(self,_url,payload):
        r = requests.put(_url,data=payload,headers=self.headers, timeout=self.timeout)
        return r

    def postRest(self,_url,payload):
        r = requests.post(_url,data=payload,headers=self.headers, timeout=self.timeout)
        return r

    def deleteRest(self,_url):
        r = requests.delete(_url,data=None,headers=self.headers, timeout=self.timeout)
        return r

    def request_inspection_get_headers(self):
        _url = f"{self.server}headers"
        return self.getRest(_url)

    def request_inspection_get_ip(self):
        _url = f"{self.server}ip"
        return self.getRest(_url)


    def response_inspection_post_response_headers(self,payload={}):
        _url = f"{self.server}response-headers"
        return self.postRestQuery(_url,payload)

    def anything_put_anything(self,anything=""):
        _url = f"{self.server}anything/{anything}"
        return self.putRest(_url,None)

    def anything_delete_anything(self,anything=""):
        _url = f"{self.server}anything/{anything}"
        return self.deleteRest(_url)



    def resp_good(self,r):
        assert r.status_code == 200



class TestHttpBin (unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # generally speaking using a global variable is a poor pracitice
        # normally I would use a very diff framework == pytest and skirt around this
        # but its much cleaner to encounter the global object of client then constantly employing
        # >> self.client
        global client
        client = BinOrgApi()

    # simple but helpfull unit test methods
    #def setUp(self):
    #    print("setUp")

    #def tearDown(self):
    #    print("tearDown")


    #
    # lets test a few sample calls with tests trying to get in some
    #   api methiod variations Get, Post, Put, Delete ...
    #   unfortunatley this api is a bit odd and will alter paths in post and put which isnt standard
    #   so the wrapped client calls are a bit odd and parameters will be limited
    #
    def test_getHeaders(self):
        r = client.request_inspection_get_headers()
        client.resp_good(r)
        # assert on 'Host'
        assert client.host == r.json()['headers']['Host']

    def test_getIp(self):
        r = client.request_inspection_get_ip()
        pprint(r.json())

    def test_PostRespHeaders(self):
        r = client.response_inspection_post_response_headers({'sheldon':'bazinga'})
        assert r.json()['freeform'] == 'sheldon=bazinga'
        client.resp_good(r)

    def test_anything_put_anything(self):
        r = client.anything_put_anything("joemama")
        client.resp_good(r)
        assert r.json()['url'] == r.url

    def test_anything_delete_anything(self):
        r = client.anything_delete_anything("joemama")
        client.resp_good(r)
        bkpoint()
        assert r.json()['url'] == r.url




if __name__ == '__main__':
    unittest.main()
