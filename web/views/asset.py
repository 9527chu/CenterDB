from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from repository import models
from repository.models import *
from ..forms.asset import *

from importlib import import_module


class AssetCreateView(CreateView):
    model = Asset
    form_class = AssetCreateForm
    template_name = 'assets/asset_create.html'
    success_url = reverse_lazy('asset_list')

    def form_valid(self, form):
        self.asset = asset = form.save()
        asset.save()
        return super(AssetCreateView, self).form_valid(form)


class AssetListView(ListView):
    model = Asset
    paginate_by = 10
    context_object_name = 'asset_list'
    template_name = 'assets/asset_list.html'


    def get_context_data(self, **kwargs):
        assets = Asset.objects.all()
        assets_id = self.request.GET.get('assets_id', '')
        assets_id_list = [i for i in assets_id.split(',') if i.isdigit()]
        context = {
            'all_assets': assets_id_list,
            'assets': assets
        }
        kwargs.update(context)
        return super(AssetListView, self).get_context_data(**kwargs)


class AssetUpdateView(UpdateView):
    model = Asset
    form_class = AssetUpdateForm
    template_name = 'assets/asset_update.html'
    success_url = reverse_lazy('asset_list')


class AssetDetailView(DetailView):
    model = Asset
    context_object_name = 'asset'
    template_name = 'assets/asset_detail.html'


class AssetDeleteView(DeleteView):
    model = Asset
    template_name = 'assets/delete_confirm.html'
    success_url = reverse_lazy('asset_list')


class ServerListView(ListView):
    model = Server
    context_object_name = 'server_list'
    template_name = 'assets/server_list.html'

    def get_context_data(self, **kwargs):
        servers = Server.objects.all()
        servers_id = self.request.GET.get('servers_id', '')
        servers_id_list = [i for i in servers_id.split(',') if i.isdigit()]
        context = {
            'all_servers': servers_id_list,
            'servers': servers
        }
        kwargs.update(context)
        return super(ServerListView, self).get_context_data(**kwargs)


class ServerCreateView(CreateView):
    model = Server
    form_class = ServerCreateForm
    template_name = 'assets/server_create.html'
    success_url = reverse_lazy('server_list')

    def form_valid(self, form):
        self.server = server = form.save()
        server.save()
        return super(ServerCreateView, self).form_valid(form)


class ServerUpdateView(UpdateView):
    model = Server
    form_class = ServerUpdateForm
    template_name = 'assets/server_update.html'
    success_url = reverse_lazy('server_list')

class ServerDeleteView(DeleteView):
    model = Server
    template_name = 'assets/delete_confirm.html'
    success_url = reverse_lazy('server_list')

class ServerDetailView(DetailView):
    model = Server
    context_object_name = 'server'
    template_name = 'assets/server_detail.html'


class IDCListView(ListView):
    model = IDC
    context_object_name = 'idc_list'
    template_name = 'assets/idc_list.html'

    def get_context_data(self, **kwargs):
        idcs = IDC.objects.all()
        idcs_id = self.request.GET.get('idcs_id', '')
        idcs_id_list = [i for i in idcs_id.split(',') if i.isdigit()]
        context = {
            'all_idcs': idcs_id_list,
            'idcs': idcs
        }
        kwargs.update(context)
        return super(IDCListView, self).get_context_data(**kwargs)


class IDCDetailView(DetailView):
    model = IDC
    context_object_name = 'idc'
    template_name = 'assets/idc_detail.html'


class DiskListView(ListView):
    model = Disk
    context_object_name = 'disk_list'
    template_name = 'assets/disk_list.html'

    def get_context_data(self, **kwargs):
        # disks = Disk.objects.all()
        mod = import_module('repository.models')
        model_name = 'Disk'
        obj = getattr(mod, model_name)
        disks = obj.objects.all()
        context = {
            'disks': disks
        }
        kwargs.update(context)
        return super(DiskListView, self).get_context_data(**kwargs)


class DiskCreateView(CreateView):
    model = Disk
    form_class = DiskCreateForm
    template_name = 'assets/disk_create.html'
    success_url = reverse_lazy('disk_list')

    def form_valid(self, form):
        self.disk = disk = form.save()
        disk.save()
        return super(DiskCreateView, self).form_valid(form)


class DiskUpdateView(UpdateView):
    model = Disk
    form_class = DiskUpdateForm
    template_name = 'assets/disk_update.html'
    success_url = reverse_lazy('disk_list')


class DiskDetailView(DetailView):
    model = Disk
    context_object_name = 'disk'
    template_name = 'assets/disk_detail.html'


class DiskDeleteView(DeleteView):
    model = Disk
    template_name = 'assets/delete_confirm.html'
    success_url = reverse_lazy('disk_list')


class MemoryListView(ListView):
    model = Memory
    context_object_name = 'memory_list'
    template_name = 'assets/memory_list.html'

    def get_context_data(self, **kwargs):
        memorys = Memory.objects.all()
        memorys_id = self.request.GET.get('memorys_id', '')
        memorys_id_list = [i for i in memorys_id.split(',') if i.isdigit()]
        context = {
            'all_memorys': memorys_id_list,
            'memorys': memorys
        }
        kwargs.update(context)
        return super(MemoryListView, self).get_context_data(**kwargs)


class MemoryCreateView(CreateView):
    model = Memory
    form_class = MemoryForm
    template_name = 'assets/memory_form.html'
    success_url = reverse_lazy('memory_list')

    def form_valid(self, form):
        self.memory = memory = form.save()
        memory.save()
        return super(MemoryCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            'action': 'create',
        }
        kwargs.update(context)
        return super(MemoryCreateView, self).get_context_data(**kwargs)

class MemoryUpdateView(UpdateView):
    model = Memory
    form_class = MemoryForm
    template_name = 'assets/memory_form.html'
    success_url = reverse_lazy('memory_list')


class MemoryDetailView(DetailView):
    model = Memory
    context_object_name = 'memory'
    template_name = 'assets/memory_detail.html'


class MemoryDeleteView(DeleteView):
    model = Memory
    template_name = 'assets/delete_confirm.html'
    success_url = reverse_lazy('memory_list')


class NICListView(ListView):
    model = NIC
    context_object_name = 'nic_list'
    template_name = 'assets/nic_list.html'

    def get_context_data(self, **kwargs):
        nics = NIC.objects.all()
        nics_id = self.request.GET.get('nics_id', '')
        nics_id_list = [i for i in nics_id.split(',') if i.isdigit()]
        context = {
            'all_nics': nics_id_list,
            'nics': nics
        }
        kwargs.update(context)
        return super(NICListView, self).get_context_data(**kwargs)


class NICCreateView(CreateView):
    model = NIC
    form_class = NICForm
    template_name = 'assets/nic_form.html'
    success_url = reverse_lazy('nic_list')

    def form_valid(self, form):
        self.nic = nic = form.save()
        nic.save()
        return super(NICCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            'action': 'create',
        }
        kwargs.update(context)
        return super(NICCreateView, self).get_context_data(**kwargs)

class NICUpdateView(UpdateView):
    model = NIC
    form_class = NICForm
    template_name = 'assets/nic_form.html'
    success_url = reverse_lazy('nic_list')



class NICDetailView(DetailView):
    model = NIC
    context_object_name = 'nic'
    template_name = 'assets/nic_detail.html'

class NICDeleteView(DeleteView):
    model = NIC
    template_name = 'assets/delete_confirm.html'
    success_url = reverse_lazy('nic_list')


def list_view(model_name, object_name):
    mod = import_module('repository.models')
    model_object = getattr(mod, model_name)

    class UnifyListView(ListView):
        model = model_object
        context_object_name = '{0}_list'.format(object_name)
        template_name = 'assets/{0}_list.html'.format(object_name)

        def get_context_data(self, **kwargs):
            objects = model_object.objects.all()
            context = {
                '{0}s'.format(object_name): objects
            }
            kwargs.update(context)
            return super(UnifyListView, self).get_context_data(**kwargs)

    return UnifyListView
