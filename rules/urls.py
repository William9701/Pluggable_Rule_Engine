"""
URL configuration for rules app.
"""

from django.urls import path
from .views import RuleCheckView, RuleListView

app_name = 'rules'

urlpatterns = [
    path('check/', RuleCheckView.as_view(), name='rule-check'),
    path('', RuleListView.as_view(), name='rule-list'),
]
