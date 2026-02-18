from django.db import models
import uuid

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=10)  # 10 digit number
    reset_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.username


class SessionCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)
