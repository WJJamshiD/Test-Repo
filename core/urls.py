from django.urls import path
from .views import link_list, link_create


urlpatterns = [
    path('create', link_create),    # havolalar/create
    path('<str:slug>', link_list),   # /areas; /tools
    path('<str:slug>/<str:type_slug>', link_list),   # /areas/design
#     path('<int:havola_idisi>', link_detail),  # havolalar/10 
#     path('<int:link_id>/update', link_update)  # localhost:8000/havolalar/54987/update
]
