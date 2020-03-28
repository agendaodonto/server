from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from app.finance.views import TransactionTypeList, TransactionTypeDetail, InflowTransactionList, InflowTransactionDetail

urlpatterns = [
    url(r'^transaction-types/$', TransactionTypeList.as_view(),
        name='transaction-types'),
    url(r'^transaction-types/(?P<pk>[0-9]+)/$', TransactionTypeDetail.as_view(),
        name='transaction-type-detail'),
    url('^inflows/(?P<clinic_id>\\d+)/$', InflowTransactionList.as_view(),
        name='inflow-transactions'),
    url('^inflows/(?P<clinic_id>\\d+)/(?P<pk>[0-9]+)/$', InflowTransactionDetail.as_view(),
        name='inflow-transaction-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
