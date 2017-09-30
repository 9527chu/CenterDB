#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
import datetime
from utils.response import BaseResponse
from utils import agorithm
# from repository import models
from repository.models import *
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q
import datetime



class HandleAsset(object):
    @staticmethod
    def process(name, server_info, user_obj):
        response = BaseResponse()
        try:
            asset_obj = Asset.objects.filter(name=name)
            if len(asset_obj) == 0:
                try:
                    asset_obj = HandleAsset.add_asset(server_info)
                    print asset_obj
                except Exception:
                    response.status = False
                    response.error = 'add asset error'
                    return response
                HandleServer.add_server(asset_obj, server_info)
            else:
                asset_obj = asset_obj[0]
                HandleAsset.update_asset(asset_obj, server_info)
                server_obj = Server.objects.filter(asset=asset_obj)
                if len(server_obj) == 0:
                    print 'create_server'
                    HandleServer.add_server(asset_obj, server_info)
                else:
                    HandleServer.update_server(asset_obj, server_info, None)
            HandleNic.process(asset_obj, server_info, None)
            HandleMemory.process(asset_obj, server_info, None)
        except Exception, e:
            response.status = False
            response.error = e
        return response


    @staticmethod
    def add_asset(server_info):
        device_status = 'on'
        device_type = 'virtual_host'
        main_board = server_info['main_board']['data']
        name = main_board['name']
        sn = main_board['sn']
        uuid = main_board['uuid']
        manufactory_str = main_board['manufacturer']
        manufactory = Manufactory.objects.get_or_create(name=manufactory_str)[0]
        log_str = '[新增资产]{name}:sn为{sn};uui为{uuid}'.format(name=name, sn=sn, uuid=uuid)
        asset = Asset.objects.create(device_status=device_status,
                                    device_type=device_type,
                                    name=name,
                                    sn=sn,
                                    uuid=uuid,
                                    manufactory=manufactory)
        AssetRecord.objects.create(asset_obj=asset, content=log_str)
        return asset

    @staticmethod
    def del_asset(server_info):
        main_board = server_info['main_board']['data']
        name = main_board['name']
        asset = Asset.objects.get(name=name)
        asset.delete()

    @staticmethod
    def update_asset(asset_obj, server_info):
        log_list = []
        main_board = server_info['main_board']['data']
        name = main_board['name']
        sn = main_board['sn']
        model = main_board['model']
        uuid = main_board['uuid']
        manufactory_str = main_board['manufacturer']
        if asset_obj.sn != main_board['sn']:
            log_list.append('SN由%s变更为%s' % (asset_obj.sn, main_board['sn'],))
            asset_obj.sn = main_board['sn']
        if asset_obj.model != main_board['model']:
            log_list.append('model由%s变更为%s' % (asset_obj.model, main_board['model']))
            asset_obj.model = main_board['model']
        if asset_obj.manufactory.name != main_board['manufacturer']:
            manufactory = Manufacoty.objects.filter(name=main_board['manufacturer'])
            if len(manufactory) == 0:
                manufactory = Manufactory.objects.create(name=main_board['manufacturer'])
            log_list.append('manufactory由%s变为%s' % (asset_obj.manufactory.name, main_board['manufacturer']))
            asset_obj.manufactory = manufactory
        asset_obj.save()
        if log_list:
            AssetRecord.objects.create(asset_obj=asset_obj, creator=user_obj,
                                              content=';'.join(log_list))









# ############# 操作基本信息（cpu和主板） #############
# 操作基本，并记录操作日志
# 更新cpu和主板信息
class HandleServer(object):
    # 处理基本信息，包括主板和CPU信息
    @staticmethod
    def process(asset_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            try:
                server = Server.objects.get(asset=asset_obj)
                HandleServer.update_server(asset_obj, server_info)
            except ObjectDoesNotExist:
                print 'add_server execute'
                HandleServer.add_server(asset_obj, server_info)
        except Exception as e:
            response.status = False
            # ErrorLog.objects.create(asset=asset_obj,
            #                                content=traceback.format_exc())
        return response


    @staticmethod
    def add_server(asset_obj, server_info):
        main_board = server_info['main_board']['data']
        cpu_info = server_info['cpu']['data']

        # for nic in server_info['nic']:
        #     if nic['ipaddrs']:
        #         if not nic['ipaddrs'].startswith(('10.0', '172.16', '192.168')):
        #             manage_ip = nic['ipaddrs']
        #             break

        data_set = {
            'asset': asset_obj,
            'hostname': server_info['hostname'],
            'model': main_board['model'],
            'kernel_release': server_info['kernel_release'],
            'os_platform': server_info['os_platform'],
            'os_version': server_info['os_version'],
            'cpu_count': cpu_info['cpu_count'],
            'cpu_physical_count': cpu_info['cpu_physical_count'],
            'cpu_model': cpu_info['cpu_model'],

        }

        print data_set
        server_obj = Server.objects.create(**data_set)
        return server_obj
        # log_str = '[新增服务器]{hostname}:model为{model};kernel_release为{kernel_release};os_platform为{os_platform};' \
        #           'os_version为{os_version};cpu_count为{cpu_count};cpu_physical_count为{cpu_physical_count};' \
        #           'cpu_model为{cpu_model}'.format(**data_set)
        # if log_str:
        #     AssetRecord.objects.create(asset=asset_obj,
        #                                       content=log_str)



    @staticmethod
    def update_server(asset_obj, server_info, user_obj):
        log_list = []
        main_board = server_info['main_board']['data']
        cpu = server_info['cpu']['data']
        server_obj = Server.objects.get(asset=asset_obj)
        if server_obj.os_platform != server_info['os_platform']:
            log_list.append('系统由%s变更为%s' % (server_obj.os_platform, server_info['os_platform'],))
            server_obj.os_platform = server_info['os_platform']

        if server_obj.os_version != server_info['os_version']:
            log_list.append(u'系统版本由%s变更为%s' % (server_obj.os_version, server_info['os_version'],))
            server_obj.os_version = server_info['os_version']

        # if server_obj.sn != main_board['sn']:
        #     log_list.append(u'主板SN号由%s变更为%s' % (server_obj.sn, main_board['sn'],))
        #     server_obj.sn = main_board['sn']

        # if server_obj.manufacturer != main_board['manufacturer']:
        #     log_list.append(u'主板厂商由%s变更为%s' % (server_obj.manufacturer, main_board['manufacturer'],))
        #     server_obj.manufacturer = main_board['manufacturer']

        if server_obj.model != main_board['model']:
            log_list.append(u'主板型号由%s变更为%s' % (server_obj.model, main_board['model'],))
            server_obj.model = main_board['model']

        if server_obj.cpu_count != cpu['cpu_count']:
            log_list.append(u'CPU逻辑核数由%s变更为%s' % (server_obj.cpu_count, cpu['cpu_count'],))
            server_obj.cpu_count = cpu['cpu_count']

        if server_obj.cpu_physical_count != cpu['cpu_physical_count']:
            log_list.append(
                u'CPU物理核数由%s变更为%s' % (server_obj.cpu_physical_count, cpu['cpu_physical_count'],))
            server_obj.cpu_physical_count = cpu['cpu_physical_count']

        if server_obj.cpu_model != cpu['cpu_model']:
            log_list.append(u'CPU型号由%s变更为%s' % (server_obj.cpu_model, cpu['cpu_model'],))
            server_obj.cpu_model = cpu['cpu_model']

        server_obj.save()
        if log_list:
            AssetRecord.objects.create(asset=asset_obj, creator=user_obj,
                                              content=';'.join(log_list))

    # @staticmethod
    # def update_last_time(server_obj, user_obj):
    #     response = BaseResponse()
    #     try:
    #         current_date = datetime.date.today()
    #         server_obj.asset.latest_date = current_date
    #         server_obj.asset.save()
    #         AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content='资产汇报')
    #     except Exception as e:
    #         response.status = False
    #         ErrorLog.objects.create(asset_obj=server_obj.asset, title='basic-run',
    #                                        content=traceback.format_exc())
    #
    #     return response


# ############# 操作网卡信息 #############
# 操作网卡，并记录操作日志
# 添加网卡
# 删除网卡
# 更新网卡信息
class HandleNic(object):
    @staticmethod
    def process(asset_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            nic_info = server_info['nic']
            if not nic_info['status']:
                response.status = False
                ErrorLog.objects.create(asset=asset_obj, title='nic-agent', content=nic_info['error'])
                return response

            client_nic_dict = nic_info['data']
            nic_obj_list = NIC.objects.filter(asset=asset_obj)
            nic_name_list = map(lambda x: x, (item.name for item in nic_obj_list))

            update_list = agorithm.get_intersection(set(client_nic_dict.keys()), set(nic_name_list))
            add_list = agorithm.get_exclude(client_nic_dict.keys(), update_list)
            del_list = agorithm.get_exclude(nic_name_list, update_list)

            HandleNic._add_nic(add_list, client_nic_dict, asset_obj, user_obj)
            HandleNic._update_nic(update_list, nic_obj_list, client_nic_dict, asset_obj, user_obj)
            HandleNic._del_nic(del_list, nic_obj_list, asset_obj, user_obj)

        except Exception as e:
            response.status = False
            ErrorLog.objects.create(asset=asset_obj, title='nic-run', content=traceback.format_exc())

        return response

    @staticmethod
    def _add_nic(add_list, client_nic_dict, asset_obj, user_obj):
        for item in add_list:
            cur_nic_dict = client_nic_dict[item]
            cur_nic_dict['name'] = item
            log_str = '[新增网卡]{name}:mac地址为{hwaddr};状态为{up};掩码为{netmask};IP地址为{ipaddrs}'.format(**cur_nic_dict)
            cur_nic_dict['asset'] = asset_obj
            NIC.objects.create(**cur_nic_dict)
            AssetRecord.objects.create(asset_obj=sset_obj, creator=user_obj, content=log_str)


    @staticmethod
    def _del_nic(del_list, nic_objs, asset_obj, user_obj):
        for item in nic_objs:
            if item.name in del_list:
                log_str = '[移除网卡]{name}:mac地址为{hwaddr};状态为{up};掩码为{netmask};IP地址为{ipaddrs}'.format(**item.__dict__)
                item.delete()
                AssetRecord.objects.create(asset_obj=asset_obj, creator=user_obj, content=log_str)


    @staticmethod
    def _update_nic(update_list, nic_objs, client_nic_dict, asset_obj, user_obj):

        for item in nic_objs:
            if item.name in update_list:
                log_list = []

                new_hwaddr = client_nic_dict[item.name]['hwaddr']
                if item.hwaddr != new_hwaddr:
                    log_list.append(u"[更新网卡]%s:mac地址由%s变更为%s" % (item.name, item.hwaddr, new_hwaddr))
                    item.hwaddr = new_hwaddr
                new_up = client_nic_dict[item.name]['up']
                if item.up != new_up:
                    log_list.append(u"[更新网卡]%s:状态由%s变更为%s" % (item.name, item.up, new_up))
                    item.up = new_up

                new_netmask = client_nic_dict[item.name]['netmask']
                if item.netmask != new_netmask:
                    log_list.append(u"[更新网卡]%s:掩码由%s变更为%s" % (item.name, item.netmask, new_netmask))
                    item.netmask = new_netmask

                new_ipaddrs = client_nic_dict[item.name]['ipaddrs']
                if item.ipaddrs != new_ipaddrs:
                    log_list.append(u"[更新网卡]%s:IP地址由%s变更为%s" % (item.name, item.ipaddrs, new_ipaddrs))
                    item.ipaddrs = new_ipaddrs

                item.save()
                # if log_list:
                #     AssetRecord.objects.create(asset_obj=sset_obj.id, creator=user_obj,
                #                                       content=';'.join(log_list))


# ############# 操作内存信息 #############
# 操作内存，并记录操作日志
# 添加内存
# 删除内存
# 更新内存信息
class HandleMemory(object):
    @staticmethod
    def process(asset_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            mem_info = server_info['memory']
            if not mem_info['status']:
                ErrorLog.objects.create(asset_obj=asset_obj, title='memory-agent',
                                               content=mem_info['error'])
                response.status = False
                return response

            client_mem_dict = mem_info['data']
            mem_obj_list = Memory.objects.filter(asset=asset_obj)

            mem_slots = map(lambda x: x, (item.slot for item in mem_obj_list))

            update_list = agorithm.get_intersection(set(client_mem_dict.keys()), set(mem_slots))
            add_list = agorithm.get_exclude(client_mem_dict.keys(), update_list)
            del_list = agorithm.get_exclude(mem_slots, update_list)

            # print 'add_mem_list: ', add_list

            HandleMemory._add_memory(add_list, client_mem_dict, asset_obj, user_obj)
            HandleMemory._update_memory(update_list, mem_obj_list, client_mem_dict, asset_obj, user_obj)
            HandleMemory._del_memory(del_list, mem_obj_list, asset_obj, user_obj)
        except Exception as e:
            response.status = False
            # ErrorLog.objects.create(asset_obj=asset_obj.id, title='memory-run',
            #                                content=traceback.format_exc())

        return response

    @staticmethod
    def _add_memory(add_list, client_mem_dict, asset_obj, user_obj):
        for item in add_list:
            cur_mem_dict = client_mem_dict[item]
            log_str = '[新增内存]插槽为{slot};容量为{capacity};类型为{model};速度为{speed};厂商为{manufacturer};SN号为{sn}'.format(
                **cur_mem_dict)
            cur_mem_dict['asset'] = asset_obj
            Memory.objects.create(**cur_mem_dict)
            # AssetRecord.objects.create(asset_obj=asset_obj.id, creator=user_obj, content=log_str)


    @staticmethod
    def _del_memory(del_list, mem_objs, asset_obj, user_obj):
        for item in mem_objs:
            if item.slot in del_list:
                log_str = '[移除内存]插槽为{slot};容量为{capacity};类型为{model};速度为{speed};厂商为{manufacturer};SN号为{sn}'.format(
                    **item.__dict__)
                item.delete()
                # AssetRecord.objects.create(asset_obj=asset_obj.id, creator=user_obj, content=log_str)


    @staticmethod
    def _update_memory(update_list, mem_objs, client_mem_dict, asset_obj, user_obj):
        for item in mem_objs:
            if item.slot in update_list:
                log_list = []

                new_manufacturer = client_mem_dict[item.slot]['manufacturer']
                if item.manufacturer != new_manufacturer:
                    log_list.append(u"[更新内存]%s:厂商由%s变更为%s" % (item.slot, item.manufacturer, new_manufacturer))
                    item.manufacturer = new_manufacturer

                new_model = client_mem_dict[item.slot]['model']
                if item.model != new_model:
                    log_list.append(u"[更新内存]%s:型号由%s变更为%s" % (item.slot, item.model, new_model))
                    item.model = new_model

                new_capacity = client_mem_dict[item.slot]['capacity']
                if item.capacity != new_capacity:
                    log_list.append(u"[更新内存]%s:容量由%s变更为%s" % (item.slot, item.capacity, new_capacity))
                    item.capacity = new_capacity

                new_sn = client_mem_dict[item.slot]['sn']
                if item.sn != new_sn:
                    log_list.append(u"[更新内存]%s:SN号由%s变更为%s" % (item.slot, item.sn, new_sn))
                    item.sn = new_sn

                new_speed = client_mem_dict[item.slot]['speed']
                if item.speed != new_speed:
                    log_list.append(u"[更新内存]%s:速度由%s变更为%s" % (item.slot, item.speed, new_speed))
                    item.speed = new_speed

                item.save()
                # if log_list:
                #     AssetRecord.objects.create(asset_obj=asset_obj.id, creator=user_obj,
                #                                       content=';'.join(log_list))


# ############# 操作硬盘信息 #############
# 操作硬盘，并记录操作日志
# 添加硬盘
# 删除硬盘
# 更新硬盘信息
class HandleDisk(object):
    @staticmethod
    def process(asset_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            disk_info = server_info['disk']
            print 'disk_info', disk_info
            if not disk_info['status']:
                response.status = False
                ErrorLog.objects.create(asset_obj=asset_obj, title='disk-agent',
                                               content=disk_info['error'])
                return response

            client_disk_dict = disk_info['data']

            disk_obj_list = Disk.objects.filter(asset=asset_obj)

            disk_slots = map(lambda x: x, (item.slot for item in disk_obj_list))

            update_list = agorithm.get_intersection(set(client_disk_dict.keys()), set(disk_slots))
            add_list = agorithm.get_exclude(client_disk_dict.keys(), update_list)
            del_list = agorithm.get_exclude(disk_slots, update_list)

            HandleDisk._add_disk(add_list, client_disk_dict, asset_obj, user_obj)
            HandleDisk._update_disk(update_list, disk_obj_list, client_disk_dict, asset_obj, user_obj)
            HandleDisk._del_disk(del_list, disk_obj_list, asset_obj, user_obj)

        except Exception as e:
            response.status = False
            # print 'serverobj', server_obj
            # ErrorLog.objects.create(asset_obj=server_obj.asset, title='disk-run', content=traceback.format_exc())
        return response

    @staticmethod
    def _add_disk(add_list, client_disk_dict, asset_obj, user_obj):
        for item in add_list:
            cur_disk_dict = client_disk_dict[item]
            log_str = '[新增硬盘]插槽为{slot};容量为{capacity};硬盘类型为{pd_type};型号为{model}'.format(**cur_disk_dict)
            cur_disk_dict['server_obj'] = server_obj
            Disk.objects.create(**cur_disk_dict)
            # AssetRecord.objects.create(asset_obj=asset_obj.id, creator=user_obj, content=log_str)


    @staticmethod
    def _del_disk(del_list, disk_objs, asset_obj, user_obj):
        for item in disk_objs:
            if item.slot in del_list:
                log_str = '[移除硬盘]插槽为{slot};容量为{capacity};硬盘类型为{pd_type};型号为{model}'.format(**item.__dict__)
                item.delete()
                # AssetRecord.objects.create(asset_obj=asset_obj.id, creator=user_obj, content=log_str)


    @staticmethod
    def _update_disk(update_list, disk_objs, client_disk_dict, asset_obj, user_obj):
        for item in disk_objs:
            if item.slot in update_list:
                log_list = []

                new_model = client_disk_dict[item.slot]['model']
                if item.model != new_model:
                    log_list.append(u"[更新硬盘]插槽为%s:型号由%s变更为%s" % (item.slot, item.model, new_model))
                    item.model = new_model

                new_capacity = client_disk_dict[item.slot]['capacity']
                new_capacity = float(new_capacity)
                if item.capacity != new_capacity:
                    log_list.append(u"[更新硬盘]插槽为%s:容量由%s变更为%s" % (item.slot, item.capacity, new_capacity))
                    item.capacity = new_capacity

                new_pd_type = client_disk_dict[item.slot]['pd_type']
                if item.pd_type != new_pd_type:
                    log_list.append(u"[更新硬盘]插槽为%s:硬盘类型由%s变更为%s" % (item.slot, item.pd_type, new_pd_type))
                    item.pd_type = new_pd_type

                item.save()
                # if log_list:
                #     AssetRecord.objects.create(asset_obj=asset_obj.id, creator=user_obj,
                #                                       content=';'.join(log_list))

