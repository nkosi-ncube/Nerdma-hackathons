from django.shortcuts import render#
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
from .serializers import ChatbotRequestSerializer,AuctionVerificationRequestSerializer,ImageProcessingRequestSerializer,VideoAnalysisRequestSerializer
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv
load_dotenv() 
key = os.getenv('OPENAI_API_KEY')
print("API KEY",key)

client = OpenAI(api_key=key)  # Ensure you have OpenAI's library installed




logger = logging.getLogger(__name__)
@api_view(['POST'])
def chatbot_view(request):
    serializer = ChatbotRequestSerializer(data=request.data)
    if serializer.is_valid():
        prompt = serializer.validated_data['prompt']
        
        try:
            # Create a chat completion
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a knowledgeable and empathetic virtual assistant designed to assist farmers with their queries and concerns. Your primary role is to provide accurate and helpful information on various topics, including:

Livestock health and behavior
Current market prices for farm products
Solutions to common farm-related issues
When the owner of the website is not available, you will be the go-to resource for farmers seeking guidance. Your responses should be clear, informative, and supportive, ensuring that farmers receive the assistance they need to manage their farms effectively.

You are adept at understanding complex farming questions and offering practical solutions, helping to bridge the gap between farmers' needs and available resources"""},
                    {"role": "user", "content": prompt}
                ]
            )
            return Response({'response': response.choices[0].message.content})
        
        except Exception as e:
            # Log the exception
            logger.error(f"Error occurred while fetching completion: {str(e)}", exc_info=True)
            # Return a generic error response
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def auction_verification(request):
    serializer = AuctionVerificationRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        image_url = serializer.validated_data['image']
        prompt = serializer.validated_data.get('prompt',  "Evaluate the health and suitability of the livestock for auction based on this image of medical record of the particular livestock. please respond with eligible or not eligible only do not explain")
        
        try:
            # Prepare the message for the OpenAI chat completion
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500
            )

            # Return the response from OpenAI
            return Response({'response': response.choices[0].message.content})
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



predefined_image_urls = [
    "https://c8.alamy.com/comp/DP5R30/peeled-banana-standing-straight-isolated-on-white-with-shadow-DP5R30.jpg",
    "https://c8.alamy.com/comp/2AA8JPM/noni-or-morinda-citrifolia-fruits-and-half-slice-isolated-on-white-background-with-clipping-path-2AA8JPM.jpg"
]
@api_view(['POST'])
def image_processing_view(request):
    serializer = ImageProcessingRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        # Get the single image URL from the request
        single_image_url = serializer.validated_data['image']
        
        # Combine with predefined image URLs
        image_urls = [single_image_url] + predefined_image_urls
        
        try:
            # Prepare the messages for the OpenAI chat completion
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What are in these images? And which images match?",
                        }
                    ] + [
                        {
                            "type": "image_url",
                            "image_url": {"url": url}
                        } for url in image_urls
                    ]
                }
            ]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=300
            )
            print(response)

            # Return the response from OpenAI
            return Response({'response': response.choices[0].message.content})
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .utils import analyze_video  # Make sure to implement this function

@api_view(['POST'])
def video_analysis_view(request):
    serializer = VideoAnalysisRequestSerializer(data=request.data)
    if serializer.is_valid():
        video_data = serializer.validated_data['video']
        results = analyze_video(video_data)
        return Response(results)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def iot_data_view(request):
    response = requests.get('https://iot-service.example.com/livestock-data')
    data = response.json()
    return Response(data)