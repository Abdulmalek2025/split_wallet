from django.urls import path
from .views import ReportView,download_file, filter_user, filter_category,filter_start, filter_end

urlpatterns = [
    path('', ReportView.as_view(), name='report'),
    path('filter-user/<int:user>',filter_user,name='filter_user'),
    path('filter-category/<int:category>',filter_category, name='filter_category'),
    path('filter-start/<str:start>',filter_start, name='filter_start'),
    path('filter-end/<str:end>', filter_end, name='filter_end'),
    path('download/',download_file,name='download_file'),
]
