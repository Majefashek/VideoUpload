from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title

    

class VideoChunk(models.Model):
    video_file = models.FileField(upload_to='video_chunks/')
    created_at = models.DateTimeField(auto_now_add=True)
    video=models.ForeignKey(Video,  on_delete=models.SET_NULL,null=True, blank=True)

    

