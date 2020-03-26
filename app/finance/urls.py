from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from app.finance.views.transaction_type import TransactionTypeList, TransactionTypeDetail

urlpatterns = [
    url(r'^transaction-types/$', TransactionTypeList.as_view(), name='transaction-types'),
    url(r'^transaction-types/(?P<pk>[0-9]+)$', TransactionTypeDetail.as_view(), name='transaction-type-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
