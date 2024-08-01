from django.urls import path
from .views import chatbot_view,auction_verification,image_processing_view,video_analysis_view,iot_data_view

urlpatterns = [
    path('chatbot/', chatbot_view, name='chatbot'),
    path('auction-analysis/', auction_verification, name='auction-analysis'),
    path('image-processing/', image_processing_view, name='image-processing'),
path('video-analysis/', video_analysis_view, name='video-analysis'),
 path('iot-data/', iot_data_view, name='iot-data'),
]