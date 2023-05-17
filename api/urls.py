# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'master_traders', views.MasterTraderViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('master_traders1/<str:source>/<str:external_trader_id>/', views.MasterTraderRetrieveView.as_view(),
         name='master_trader_retrieve'),

]
