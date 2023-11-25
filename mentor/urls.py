# 3rd Party Import
from django.urls import path

# Local Import
from .views import dashboard, delete_research_area, update_research_area, add_research_area

urlpatterns = [
    path('dashboard/', dashboard, name="mentor_dashboard"),
    path('add_research_area/', add_research_area, name="add_research_area"),
    path('delete_research_area/', delete_research_area, name="delete_research_area"),
    path('update_research_area/', update_research_area, name="update_research_area"),
]