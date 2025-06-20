from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Optional fields
    tags = models.CharField(max_length=255, blank=True)
    pinned = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    color = models.CharField(max_length=20, blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.title 