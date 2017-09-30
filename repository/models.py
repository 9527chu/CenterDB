#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='邮箱',
        max_length=255,
        unique=True,
    )
    username = models.CharField(verbose_name='用户名', unique=True, max_length=64)
    is_active = models.BooleanField(verbose_name='是否激活', default=True)
    is_admin = models.BooleanField(verbose_name='是否管理员', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name_plural = "用户"


class UserGroup(models.Model):
    """
    用户组
    """
    name = models.CharField(max_length=32, unique=True)
    users = models.ManyToManyField('User')

    class Meta:
        verbose_name_plural = "用户组"

    def __str__(self):
        return self.name


class BusinessUnit(models.Model):
    """
    业务线
    """
    name = models.CharField('业务线', max_length=64, unique=True)
    contact = models.ForeignKey('UserGroup', verbose_name='业务联系人', related_name='c', blank=True, null=True)
    manager = models.ForeignKey('UserGroup', verbose_name='系统管理员', related_name='m', blank=True, null=True)

    class Meta:
        verbose_name_plural = "业务线"

    def __str__(self):
        return self.name


class Operator(models.Model):
    """
    运营商表   例如：电信 联通 教育网 长城宽带等
    被机房关联。本身不关联任何表 只记录
    """
    name = models.CharField('运营商', max_length=64, unique=True)
    memo = models.CharField('备注', max_length=128, blank=True,null=True)

    class Meta:
        verbose_name = '运营商'
        verbose_name_plural = "运营商"

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房表结构 关联合同和运营商
    机房表需要机房联系人 联系电话 机房的基本信息等
    """
    name = models.CharField(u'机房名称', max_length=64, unique=True)
    contacts = models.CharField('机房技术', max_length=63, null=True, blank=True)
    idc_phone = models.IntegerField('机房电话', null=True, blank=True)
    contacts_phone = models.IntegerField('联系人电话', null=True, blank=True)
    contacts_qq = models.IntegerField('机房技术QQ', null=True, blank=True)
    idc_addr = models.CharField('机房地址', max_length=63, null=True, blank=True)
    bandwidth = models.CharField('机房带宽', max_length=63, null=True, blank=True)
    operator = models.ForeignKey('Operator', verbose_name=u'运营商', null=True, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Tag(models.Model):
    """
    资产标签
    """
    name = models.CharField('标签', max_length=32, unique=True)

    class Meta:
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    asset_type_choices = (
        ('physical_host', '物理机'),
        ('virtual_host', '虚拟机'),
        ('cloud_host', '云主机'),
        ('switch', '交换机'),
        ('router', '路由器'),
        ('firewall', '防火墙'),
        ('storage', '防火墙'),
        ('others', '其他'),
    )
    asset_status_choices = (
        ('on', '上架'),
        ('on_line', '在线'),
        ('off_line', '离线'),
        ('off', '下架'),
    )

    device_type = models.CharField(verbose_name='资产类型', choices=asset_type_choices, max_length=64, default='virtual_host')
    device_status = models.CharField(verbose_name='资产状态', choices=asset_status_choices, max_length=64, default='on')
    name = models.CharField(verbose_name='资产名称', max_length=64, blank=True, null=True, unique=True)
    sn = models.CharField('资产SN号', max_length=128, null=True, blank=True)
    uuid = models.CharField('UUID', max_length=64, unique=True, null=True)
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', null=True, blank=True)
    cabinet_num = models.CharField('机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField('机柜中序号', max_length=30, null=True, blank=True)
    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='属于的业务线', null=True, blank=True)
    tag = models.ManyToManyField('Tag', blank=True)
    memo = models.TextField('备注', null=True, blank=True)
    update_date = models.DateField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产"

    # def __str__(self):
    #     return str(self.name)


class Server(models.Model):
    """
    服务器信息
    """

    asset = models.OneToOneField('Asset', related_name='server')

    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)
    hostname = models.CharField(max_length=128)
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField('管理IP', null=True, blank=True)

    kernel_release = models.CharField(u'内核', max_length=128, null=True, blank=True)
    os_platform = models.CharField('系统', max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)

    memo = models.TextField('备注', null=True, blank=True)
    update_date = models.DateTimeField('更新日期', auto_now=True, blank=True)
    create_date = models.DateTimeField('添加日期', auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "服务器"

    def __str__(self):
        return self.hostname


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    management_ip = models.CharField('管理IP', max_length=64, blank=True, null=True)
    vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
    intranet_ip = models.CharField('内网IP', max_length=128, blank=True, null=True)
    sn = models.CharField('SN号', max_length=64, unique=True)
    manufacture = models.ForeignKey('Manufactory', verbose_name=u'制造商', max_length=128, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
    device_detail = models.CharField('设置详细配置', max_length=255, null=True, blank=True)

    memo = models.TextField('备注', null=True, blank=True)
    update_date = models.DateTimeField('更新日期', auto_now=True, blank=True)
    create_date = models.DateTimeField('添加日期', auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "网络设备"

    def __str__(self):
        return self.vlan_ip


class Disk(models.Model):
    """
    硬盘信息
    """
    disk_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )
    asset = models.ForeignKey('Asset', related_name='disk')
    slot = models.CharField('插槽位', max_length=8)
    model = models.CharField('磁盘型号', max_length=32)
    manufactory = models.CharField(u'制造商', max_length=64, blank=True, null=True)
    capacity = models.FloatField('磁盘容量GB')
    disk_type = models.CharField('磁盘类型', choices=disk_type_choice, max_length=32, default='SATA')
    memo = models.TextField('备注', null=True, blank=True)
    update_date = models.DateTimeField('更新日期', auto_now=True, blank=True)
    create_date = models.DateTimeField('添加日期', auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "硬盘"

    def __str__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)


class RaidAdaptor(models.Model):
    """
    raid卡
    """
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插口', max_length=64)
    model = models.CharField(u'型号', max_length=64, blank=True, null=True)
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'raid卡'
        verbose_name_plural = 'raid卡'
        unique_together = ("asset", "slot")


class NIC(models.Model):
    """
    网卡信息
    """
    asset = models.ForeignKey('Asset', related_name='nic')
    name = models.CharField('网卡名称', max_length=128)
    sn = models.CharField('SN号', max_length=128, blank=True,null=True)
    model = models.CharField('网卡型号', max_length=128, blank=True,null=True)
    hwaddr = models.CharField('网卡mac地址', max_length=64)
    netmask = models.CharField('子网掩码', max_length=64)
    ipaddrs = models.CharField('ip地址', max_length=256)
    up = models.BooleanField('状态', default=False)
    memo = models.TextField('备注', null=True, blank=True)
    update_date = models.DateTimeField('更新日期', auto_now=True, blank=True)
    create_date = models.DateTimeField('添加日期', auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "网卡"

    def __str__(self):
        return self.name


class Memory(models.Model):
    """
    内存信息
    """
    asset = models.ForeignKey('Asset', related_name='memory')
    slot = models.CharField('插槽位', max_length=32)
    manufacturer = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64)
    capacity = models.FloatField('容量', null=True, blank=True)
    sn = models.CharField('内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField('速度', max_length=16, null=True, blank=True)
    memo = models.TextField('备注', null=True, blank=True)
    update_date = models.DateTimeField('更新日期', auto_now=True, blank=True)
    create_date = models.DateTimeField('添加日期', auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "内存"

    def __str__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)


class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    asset_obj = models.ForeignKey('Asset', related_name='ar')
    content = models.TextField(null=True)
    creator = models.ForeignKey('User', null=True, blank=True)
    update_date = models.DateTimeField('更新日期', auto_now=True, blank=True)
    create_date = models.DateTimeField('添加日期', auto_now_add=True, blank=True)


    class Meta:
        verbose_name_plural = "资产记录"

    # def __str__(self):
    #     return "%s-%s-%s" % (self.asset_obj.idc.name, self.asset_obj.cabinet_num, self.asset_obj.cabinet_order)
    def __str__(self):
        return self.asset_obj.name


class Manufactory(models.Model):

    """
    资产的厂商名称和支持电话
    例如保修联系
    """

    name = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=30, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    class Meta:
        verbose_name = '设备厂商'
        verbose_name_plural = "设备厂商"

    def __str__(self):
        return self.name






class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey('Asset', null=True, blank=True)
    title = models.CharField(max_length=16)
    content = models.TextField('内容')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "错误日志"

    def __str__(self):
        return self.title


class EventLog(models.Model):
    """事件"""

    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    asset = models.ForeignKey('Asset')
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    user = models.ForeignKey('User', verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.event_type == 2:
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = u'事件类型'


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, blank=True, null=True)
    manufactory = models.CharField(max_length=64, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    ram_size = models.IntegerField(blank=True, null=True)
    cpu_model = models.CharField(max_length=128, blank=True, null=True)
    cpu_count = models.IntegerField(blank=True, null=True)
    cpu_core_count = models.IntegerField(blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'汇报日期', auto_now_add=True)
    approved = models.BooleanField(u'已批准', default=False)
    approved_by = models.ForeignKey('User', verbose_name=u'批准人', blank=True, null=True)
    approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"