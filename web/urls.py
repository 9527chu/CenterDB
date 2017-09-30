from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from views import account, asset



urlpatterns = [
    url(r'^login$', account.LoginView.as_view(), name='login'),
    url(r'^logout$', account.LogoutView.as_view(), name='logout'),
    url(r'^index$', account.IndexView.as_view(), name='index'),

    url(r'^asset/list$', asset.AssetListView.as_view(), name='asset_list'),
    url(r'^asset/create$', asset.AssetCreateView.as_view(), name='asset_create'),
    url(r'^asset/(?P<pk>[0-9]+)/update$', asset.AssetUpdateView.as_view(), name='asset_update'),
    url(r'^asset/(?P<pk>[0-9]+)/detail$', asset.AssetDetailView.as_view(), name='asset_detail'),
    url(r'^asset/(?P<pk>[0-9]+)/delete$', asset.AssetDeleteView.as_view(), name='asset_delete'),

    url(r'^server/list', asset.ServerListView.as_view(), name='server_list'),
    url(r'^server/create', asset.ServerCreateView.as_view(), name='server_create'),
    url(r'^server/(?P<pk>[0-9]+)/update', asset.ServerUpdateView.as_view(), name='server_update'),
    url(r'^server/(?P<pk>[0-9]+)/delete', asset.ServerDeleteView.as_view(), name='server_delete'),
    url(r'^server/(?P<pk>[0-9]+)/detail', asset.ServerDetailView.as_view(), name='server_detail'),

    url(r'^disk/list', asset.DiskListView.as_view(), name='disk_list'),
    url(r'^disk/create', asset.DiskCreateView.as_view(), name='disk_create'),
    url(r'^disk/(?P<pk>[0-9]+)/update', asset.DiskUpdateView.as_view(), name='disk_update'),
    url(r'^disk/(?P<pk>[0-9]+)/delete', asset.DiskDeleteView.as_view(), name='disk_delete'),
    url(r'^disk/(?P<pk>[0-9]+)/detail', asset.DiskDetailView.as_view(), name='disk_detail'),

    #url(r'^memory/list', asset.MemoryListView.as_view(), name='memory_list'),
    url(r'^memory/list', asset.list_view('Memory', 'memory').as_view(), name='memory_list'),
    url(r'^memory/create', asset.MemoryCreateView.as_view(), name='memory_create'),
    url(r'^memory/(?P<pk>[0-9]+)/update', asset.MemoryUpdateView.as_view(), name='memory_update'),
    url(r'^memory/(?P<pk>[0-9]+)/delete', asset.MemoryDeleteView.as_view(), name='memory_delete'),
    url(r'^memory/(?P<pk>[0-9]+)/detail', asset.MemoryDetailView.as_view(), name='memory_detail'),

    url(r'^nic/list', asset.NICListView.as_view(), name='nic_list'),
    url(r'^nic/create', asset.NICCreateView.as_view(), name='nic_create'),
    url(r'^nic/(?P<pk>[0-9]+)/update', asset.NICUpdateView.as_view(), name='nic_update'),
    url(r'^nic/(?P<pk>[0-9]+)/delete', asset.NICDeleteView.as_view(), name='nic_delete'),
    url(r'^nic/(?P<pk>[0-9]+)/detail', asset.NICDetailView.as_view(), name='nic_detail'),
    #
    # url(r'^raid/list', asset.RaidListView.as_view(), name='raid_list'),
    # url(r'^raid/create', asset.RaidCreateView.as_view(), name='raid_create'),
    # url(r'^raid/(?P<pk>[0-9]+)/update', asset.RaidUpdateView.as_view(), name='raid_update'),
    # url(r'^raid/(?P<pk>[0-9]+)/delete', asset.RaidUpdateView.as_view(), name='raid_delete'),
    # url(r'^raid/(?P<pk>[0-9]+)/detail', asset.RaidDetailView.as_view(), name='raid_detail'),



    url(r'^idc/list', asset.IDCListView.as_view(), name='idc_list'),
    url(r'^idc/(?P<pk>[0-9]+)/detail', asset.IDCDetailView.as_view(), name='idc_detail'),

]