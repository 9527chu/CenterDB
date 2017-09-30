#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import importlib
from django.views import View
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

from utils import auth
from dbi import config
from repository import models
from dbi.service import asset
from dbi.service.asset import *


class AssetView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AssetView, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth.api_auth)
    def get(self, request, *args, **kwargs):
        """
        获取今日未更新的资产 - 适用SSH或Salt客户端
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # test = {'user': '用户名', 'pwd': '密码'}
        # result = json.dumps(test,ensure_ascii=True)
        # result = json.dumps(test,ensure_ascii=False)
        # return HttpResponse(result)

        # test = {'user': '用户名', 'pwd': '密码'}
        # result = json.dumps(test,ensure_ascii=True)
        # result = json.dumps(test,ensure_ascii=False)
        # return HttpResponse(result,content_type='application/json')

        # test = {'user': '用户名', 'pwd': '密码'}
        # return JsonResponse(test, json_dumps_params={"ensure_ascii": False})

        response = asset.get_untreated_servers()
        return JsonResponse(response.__dict__)

    @method_decorator(auth.api_auth)
    def post(self, request, *args, **kwargs):
        """
        更新或者添加资产信息
        :param request:
        :param args:
        :param kwargs:
        :return: 1000 成功;1001 接口授权失败;1002 数据库中资产不存在
        """

        server_info = json.loads(request.body.decode('utf-8'))
        server_info = json.loads(server_info)

        hostname = server_info['hostname']
        name = server_info['main_board']['data']['name']
        print name
        print server_info
        ret = {'code': 1000, 'message': '[%s]更新完成' % hostname}

        # try:
        #     asset_obj = models.Asset.objects.get(name=name)
        # except ObjectDoesNotExist:
        #     asset_obj = HandleAsset._add_asset(server_info)
        #     print dir(asset_obj)
        # server_obj = asset_obj.server
        # print asset_obj.memory
        # print asset_obj.server
        # print asset_obj.nic
        # print asset_obj.disk
        # server_obj = models.Server.objects.filter(hostname=hostname).select_related('asset').first()
        # if not server_obj:
        #     ret['code'] = 1002
        #     ret['message'] = '[%s]资产不存在' % hostname
        #     return JsonResponse(ret)

        res = HandleAsset.process(name, server_info, None)
        # print res.__dict__
        # for k, v in config.PLUGINS_DICT.items():
        #     module_path, cls_name = v.rsplit('.', 1)
        #     cls = getattr(importlib.import_module(module_path), cls_name)
        #     response = cls.process(name, server_info, None)
        #     if not response.status:
        #         ret['code'] = 1003
        #         ret['message'] = "[%s]资产更新异常" % hostname
        #     if hasattr(cls, 'update_last_time'):
        #         cls.update_last_time(server_obj, None)
        print res.__dict__
        return JsonResponse(ret)

