from django.urls import path
from .views import ReportView,download_file, filter_user, filter_category,filter_start, filter_end
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', login_required(ReportView.as_view()), name='report'),
    path('filter-user/<int:user>',login_required(filter_user),name='filter_user'),
    path('filter-category/<int:category>',login_required(filter_category), name='filter_category'),
    path('filter-start/<str:start>',login_required(filter_start), name='filter_start'),
    path('filter-end/<str:end>', login_required(filter_end), name='filter_end'),
    path('download/',login_required(download_file),name='download_file'),
]
