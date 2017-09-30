from views.asset import *
from rest_framework import renderers
from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'assets', AssetViewSet)
router.register(r'servers', ServerViewSet)
router.register(r'networkdevices', NetworkDeviceSet)
router.register(r'disks', DiskViewSet)
router.register(r'raids', RaidAdaptorViewSet)
router.register(r'nics', NICViewSet)
router.register(r'memorys', MemoryViewSet)
router.register(r'idcs', IDCViewSet)
router.register(r'businessunits', BusinessUnitViewSet)
router.register(r'perators', OperatorViewSet)
router.register(r'manufactories', ManufactoryViewSet)
router.register(r'tagos', TagViewSet)

urlpatterns = [
    url(r'assets/$', AssetListView.as_view(), name='asset-list'),
    url(r'assets/(?P<pk>[0-9]+)/$', AssetDetailView.as_view(), name='asset-detail'),
    url(r'', include(router.urls)),
]