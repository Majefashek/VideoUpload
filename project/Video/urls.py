
from django.urls import path, include
from . import views
urlpatterns = [
    path('create_video',views.CreateVideo, name="create_video"),
    path('upload_video_chunk',views.upload_video_chunk, name="upload_chunk"),
    path('retrieve_video/<int:video_id>',views.retrieveVideo, name="retrieve_video"),
    #path('get/<int:id>', GetVideoAPIView.as_view(), name="get")

]
