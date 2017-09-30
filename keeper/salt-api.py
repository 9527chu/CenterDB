#!/usr/bin/env python
# coding: utf-8

import requests
import json

import ssl
context = ssl._create_unverified_context()

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


salt_url = '192.168.245.129'
salt_port = 8080


class SaltApi:
    def __init__(self, salt_url, port, response_format='json'):
        self.salt_url = salt_url
        self.port = port
        self.username = "saltapi"
        self.password = "123123"
        self.response_format = response_format
        self.ori_request_str = "https://{0}:{1}".format(self.salt_url, self.port)
        self.login_request_str = self.ori_request_str + '/' + 'login'
        self.login_data = dict(username=self.username, password=self.password, eauth="pam")
        self.common_data = dict(client='local')
        self.async_common_data = dict(client='local_async')
        self.key_data = dict(client='wheel')
        self.headers = {
           "Content-Type" : "application/json",
           "Accept" : "application/{0}".format(self.response_format),
        }
        self.token = self.get_token()

    def get(self, request_str, data=None):
        res = requests.get(request_str, headers=self.headers, data=data, verify=False)
        return res

    def post(self, request_str, data=None):
        res = requests.post(request_str, headers=self.headers, data=data, verify=False)
        return res
   
    def get_token(self):
        res = self.post(self.login_request_str, data=json.dumps(self.login_data)).content
        res = json.loads(res).get("return")[0].get("token", "")
        self.token = res
        return self.token

    def get_data(self, tgt, fun, arg=None, async=False):
        if async:
            self.common_data = self.async_common_data
        if arg:
            self.common_data.update({"tgt":tgt, "fun":fun, "arg":arg})
        else:
            self.common_data.update({"tgt":tgt, "fun":fun})
        self.headers.update({"Accept" : "application/json", "X-Auth-Token": self.token})
        res = self.post(self.ori_request_str, data=json.dumps(self.common_data)).content
        return res
    
    
    def get_all_keys(self): 
        self.key_data.update({"fun":"key.list_all"})
        self.headers.update({"Accept" : "application/json", "X-Auth-Token": self.token})
        res = self.post(self.ori_request_str, data=json.dumps(self.key_data)).content
        res_pre = json.loads(res)["return"][0]["data"]["return"]
        minions = res_pre["minions"]
        minions_pre = res_pre["minions_pre"]
        minions_rej = res_pre["minions_rejected"]
        minions_deni = res_pre["minions_denied"]
        return minions, minions_pre

    def accept_key(self, node):
        self.key_data.update({"fun":"key.accept", "match":node})
        self.headers.update({"Accept" : "application/json", "X-Auth-Token": self.token})
        res = self.post(self.ori_request_str, data=json.dumps(self.key_data)).content
        res = json.loads(res)["return"][0]["data"]["success"]
        return res

    def delete_key(self, node):
        self.key_data.update({"fun":"key.delete", "match":node})
        self.headers.update({"Accept" : "application/json", "X-Auth-Token": self.token})
        res = self.post(self.ori_request_str, data=json.dumps(self.key_data)).content
        res = json.loads(res)["return"][0]["data"]["success"]
        return res

    
    def reject_key(self, node):
        self.key_data.update({"fun":"key.reject", "match":node})
        self.headers.update({"Accept" : "application/json", "X-Auth-Token": self.token})
        res = self.post(self.ori_request_str, data=json.dumps(self.key_data)).content
        res = json.loads(res)["return"][0]["data"]["success"]
        return res

    def get_grains_item(self, tgt, arg):
        return self.get_data(tgt, "grains.item", arg)
 
    def get_grains(self, tgt, arg):
        return json.dumps(json.loads(self.get_data(tgt, "grains.items"))["return"][0])

    def cmd_run(self, tgt, arg):
        return self.get_data(tgt, "cmd.run", arg)

    def state(self, tgt, arg):
        return self.get_data(tgt, "state.sls", arg)

    def async_state(self, tgt, arg, async=True):
        pre_res = json.loads(self.get_data(tgt, "state.sls", arg, async))
        jid = pre_res["return"][0]["jid"]
        res = self.lookup_jid(jid)
        return res


    def lookup_jid(self, jid):
        self.common_data.update({"client":"runner", "fun":"jobs.lookup_jid" ,"jid": jid})
        self.headers.update({"Accept" : "application/json", "X-Auth-Token": self.token})
        res = self.post(self.ori_request_str, data=json.dumps(self.common_data)).content
        return res

    def get_status(self, arg):
        self.common_data.update({"client":"runner", "fun":"manage." + arg})
        self.headers.update({"Accept" : "application/x-yaml", "X-Auth-Token": self.token})
        res = self.post(self.ori_request_str, data=json.dumps(self.common_data)).content
        return res


if __name__ == '__main__':
    sa = SaltApi(salt_url, salt_port)
   # print sa.get_token()
   # print sa.get_data("*", "test.ping", "")
   # print sa.get_data("*", "grains.item", "os")
   # print sa.get_all_keys()
   # print sa.delete_key("salt-minion-1")
    print sa.get_grains("*", "pwd")
   # print sa.cmd_run("*", "pwd")
   # print sa.async_state("*", "dns")
   # print sa.lookup_jid('20170824140344535723')
   # print sa.get_status("status")


