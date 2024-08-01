from rest_framework import serializers

class ChatbotRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=1000)


class AuctionVerificationRequestSerializer(serializers.Serializer):
    image = serializers.CharField()  # Assuming image is provided as a URL
    prompt = serializers.CharField()  # Optional prompt for analysis


class ImageProcessingRequestSerializer(serializers.Serializer):
    image = serializers.CharField()  # Base64 encoded image

class VideoAnalysisRequestSerializer(serializers.Serializer):
    video = serializers.CharField()  # Base64 encoded video

class IoTDataResponseSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    heart_rate = serializers.FloatField()
    # Add more fields as required
