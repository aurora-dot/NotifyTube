from django.db import models  # nopycln: import


# Create your models here.
class YouTubeQuery(models.Model):
    query = models.CharField(max_length=500, unique=True)
    last_fetched = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    latest = models.ForeignKey(
        "YouTubeVideo",
        related_name="youtube_queries",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class YouTubeVideo(models.Model):
    video_id = models.CharField(max_length=22, unique=True)
    link = models.URLField()
    title = models.CharField(max_length=100)
    thumbnail = models.URLField()
    youtube_query = models.ForeignKey(
        YouTubeQuery, related_name="youtube_videos", on_delete=models.CASCADE
    )
    youtube_channel = models.ForeignKey(
        "YouTubeChannel", related_name="youtube_videos", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class YouTubeChannel(models.Model):
    channel_link = models.URLField(unique=True)
    channel_name = models.CharField(max_length=64)
    channel_img = models.URLField()
