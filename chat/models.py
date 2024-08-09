from django.db import models


# Create your models here.
class ChatMessage(models.Model):
    SENDER_OPTIONS = {
        ("USR", "User"),
        ("SYS", "System"),
    }
    sender = models.CharField(max_length=6, choices=SENDER_OPTIONS)
    content = models.CharField(max_length=10000)

    def serialize(self):
        return {
            "sender": self.get_sender_display(),
            "content": self.content,
        }
