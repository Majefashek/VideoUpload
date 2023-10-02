# VideoUpload

1. CreateVideo API
URL: /api/create_video

Method: POST

Description: This API allows you to create a new video entry by providing a title and description for the video.

Request Payload:

json
Copy code
{
    "title": "Your Video Title",
    "description": "Your Video Description"
}
Response:

HTTP Status: 200 OK if successful.
JSON Response:
json
Copy code
{
    "message": "Video created Successfully",
    "data": {
        "id": 1, // ID of the newly created video
        "title": "Your Video Title",
        "description": "Your Video Description"
        // Other video attributes
    }
}
2. upload_video_chunk API
URL: /api/upload_video_chunk

Method: POST

Description: This API allows you to upload video chunks for a specific video.

Request Payload:

video_id: ID of the video to which the chunk belongs.
video_chunk: The video chunk file to be uploaded.
Response:

HTTP Status: 200 OK if the chunk is uploaded successfully.
JSON Response:
json
Copy code
{
    "status": "success"
}
3. retrieveVideo API
URL: /api/retrieve_video/<video_id>

Method: GET

Description: This API allows you to retrieve and stream a complete video by combining its chunks. It returns the video as a base64-encoded string within a JSON response.

URL Parameters:

video_id: The ID of the video you want to retrieve.
Response:

HTTP Status: 200 OK if successful.
JSON Response:
json
Copy code
{
    "data": "base64_encoded_video_data"
}
Note: You can use the base64-encoded video data to display or download the video on the client side.


