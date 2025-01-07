from django.db import models

from . import SectionItem, ItemTypeChoices
from ..constants import VIDEO_TRANSCRIPT_MAX_LEN

class Video(SectionItem):
    source = models.ForeignKey(
        "Source", on_delete=models.CASCADE, related_name="videos"
    )
    transcript = models.TextField(
        null=True, blank=True, max_length=VIDEO_TRANSCRIPT_MAX_LEN,
        help_text="Transcript of the video."
    )
    start_time = models.PositiveIntegerField(help_text="Start time of the video in seconds.")
    end_time = models.PositiveIntegerField(help_text="End time of the video in seconds.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "start_time", "end_time"], name="unique_video_segment"
            )
        ]


    def save(self, *args, **kwargs):
        self.item_type = ItemTypeChoices.VIDEO
        super().save(*args, **kwargs)
