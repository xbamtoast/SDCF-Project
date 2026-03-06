from django.urls import include, path
from . import views

url_patterns = [
        path('', views.home, name='home'),
# EXAMPLE URL FROM MY PERSONAL PROJECT
        # path('seasons/', views.season_list, name='season-list'),
]