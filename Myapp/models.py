from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidate_photos/')  # Path for storing candidate photos

    def __str__(self):
        return self.name

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="votes")
    ip_address = models.GenericIPAddressField(unique=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.candidate.name} from {self.ip_address}"
