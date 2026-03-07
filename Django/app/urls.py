from django.urls import include, path
from . import views


urlpatterns = [
    # EXAMPLE URL FROM MY PERSONAL PROJECT
        # path('seasons/', views.season_list, name='season-list'),
    path('', views.home, name='home'),
    path('recipient_agreement/', views.recipient_agreement, name='recipient_agreement'),
    path('w9_upload/', views.w9_upload, name='w9_upload'),
]