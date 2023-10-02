
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated 
from django.db.models import OuterRef, Exists
from .models import Video
from .serializers import VideoSerializer
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import JsonResponse,StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Video, VideoChunk
from .serializers import VideoSerializer
from rest_framework.decorators import api_view
import os
import tempfile
import io
import base64




@csrf_exempt
@api_view(['POST'])
def CreateVideo(request):
    if request.method=="POST":
        title=request.data.get('title')
        description=request.data.get('description')
        video=Video.objects.create(title=title, description=description)
        video.save()
        videoSerialized=VideoSerializer(video)
        return Response({'message':'Video created Successfully',
                         'data':videoSerialized.data})


@csrf_exempt
@api_view(['POST'])
def upload_video_chunk(request):
     if request.method == 'POST':
        video_id=request.data.get('video_id')
        video=Video.objects.get(id=video_id)
        video_chunk = request.FILES.get('video_chunk')

        if video_chunk:
            # Save the video chunk to the server
            video_chunk_obj = VideoChunk(video_file=video_chunk,video=video)
            video_chunk_obj.save()

            return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'status': 'error', 'message': 'No video chunk provided'}, status=status.HTTP_400_BAD_REQUEST)
        

@csrf_exempt
@api_view(['GET'])
def  retrieveVideo(request, video_id):
    def combine_video_chunks(chunk_files, output_path):
        with open(output_path, 'wb') as output_file:
            for chunk in chunk_files:
                with chunk.video_file.open('rb') as chunk_file:
                    output_file.write(chunk_file.read())

    if request.method=='GET':
        # Retrieve the Video object based on the video_id
        video = get_object_or_404(Video, pk=video_id)

        # Query all related video chunks ordered by chunk number
        chunk_files = VideoChunk.objects.filter(video=video).order_by('id')
        
        
        # Define a generator function to stream video chunks
        def generate_chunks():
            for chunk in chunk_files:
                # Open and yield the content of each chunk file
                with chunk.video_file.open('rb') as file:
                    for chunk_content in file:
                        yield chunk_content
        #video_stream = generate_chunks()

        #video_response = StreamingHttpResponse(video_stream, content_type='video/mp4')
        #video_response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
        with tempfile.NamedTemporaryFile(delete=False) as combined_file:
            combine_video_chunks(chunk_files, combined_file.name)

        with open(combined_file.name, 'rb') as combined_file_content:
            file_content = combined_file_content.read()


        # Create a FileResponse to stream the video
        #response = FileResponse(generate_chunks(), content_type='video/mp4')
        #response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
        #return response
        response = FileResponse(open(combined_file.name, 'rb'), content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
        blob = io.BytesIO(file_content)

        # Encode the blob data as a Base64 string
        blob_base64 = base64.b64encode(blob.getvalue()).decode()

        # Create a JSON response with the Base64 encoded blob
        response_data = {
            "data": blob_base64
        }

        return JsonResponse(response_data)
        #data={'response':video_response}
        #return JsonResponse(data, safe=False)