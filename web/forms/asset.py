from django import forms
from django.utils.translation import gettext_lazy as _
from repository.models import *


class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'device_type', 'device_status', 'sn', 'manufactory', 'cabinet_num', 'cabinet_order',
            'idc', 'business_unit', 'tag', 'memo'
        ]
        widgets = {
            'device_type': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device_type')}),
            'device_status': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device status')}),
            'manufactory': forms.Select(
                attrs={
                    'data-placeholder': _('Select asset device status')}),
            'idc': forms.Select(
                attrs={
                    'data-placeholder': _('Select asset device status')}),
            'memo': forms.Textarea(
                attrs={
                    'data-placeholder': _('Input memo')}),
        }
        help_texts = {
            'idc': _('please select the idc '),
            'memo': _('please input the memo'),
        }

class AssetUpdateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'device_type', 'device_status', 'sn', 'manufactory', 'cabinet_num', 'cabinet_order',
            'idc', 'business_unit', 'tag', 'memo'
        ]
        widgets = {
            'device_type': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device_type')}),
            'device_status': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device status')}),
            'manufactory': forms.Select(
                attrs={
                    'data-placeholder': _('Select asset device status')}),
            'idc': forms.Select(
                attrs={
                    'data-placeholder': _('Select asset device status')}),
            'memo': forms.Textarea(
                attrs={
                    'data-placeholder': _('Input memo')}),
        }
        help_texts = {
            'idc': _('please select the idc '),
            'memo': _('please input the memo'),
        }



class ServerCreateForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = [
            'asset', 'hosted_on', 'hostname', 'manufacturer', 'model', 'manage_ip',
            'kernel_release', 'os_platform', 'os_version', 'cpu_count', 'cpu_physical_count',
            'cpu_model', 'memo'
        ]

        widgets = {
            'asset': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device_type')}),
            'hosted_on': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device status')}),
            'manufacturer': forms.Select(
                attrs={
                    'data-placeholder': _('Select asset device status')}),
            'memo': forms.Textarea(
                attrs={
                    'data-placeholder': _('Input memo')}),
        }

class ServerUpdateForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = [
            'asset', 'hosted_on', 'hostname', 'manufacturer', 'model', 'manage_ip',
            'kernel_release', 'os_platform', 'os_version', 'cpu_count', 'cpu_physical_count',
            'cpu_model', 'memo'
        ]

        widgets = {
            'asset': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device_type')}),
            'hosted_on': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device status')}),
            'manufacturer': forms.Select(
                attrs={
                    'data-placeholder': _('Select asset device status')}),
            'memo': forms.Textarea(
                attrs={
                    'data-placeholder': _('Input memo')}),
        }


class DiskCreateForm(forms.ModelForm):
    class Meta:
        model = Disk
        fields = [
            'asset', 'slot', 'model', 'manufactory', 'capacity', 'disk_type', 'memo'
        ]

        widgets = {
            'asset': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device_type')}),
            'memo': forms.Textarea(
                attrs={
                    'data-placeholder': _('Input memo')}),
        }


class DiskUpdateForm(forms.ModelForm):
    class Meta:
        model = Disk
        fields = [
            'asset', 'slot', 'model', 'manufactory', 'capacity', 'disk_type', 'memo'
        ]

        widgets = {
            'asset': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device_type')}),
            'memo': forms.Textarea(
                attrs={
                    'data-placeholder': _('Input memo')}),
        }


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = '__all__'

        widgets = {
            'asset': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device_type')}),
            'memo': forms.Textarea(
                attrs={
                    'data-placeholder': _('Input memo')}),
        }


class NICForm(forms.ModelForm):
    class Meta:
        model = NIC
        fields = '__all__'

        widgets = {
            'asset': forms.Select(
                attrs={
                       'data-placeholder': _('Select asset device_type')}),
            'memo': forms.Textarea(
                attrs={
                    'data-placeholder': _('Input memo')}),
        }