from django.contrib.auth.models import AbstractUser

# Create your models here.
# users/models.py
class CustomUser(AbstractUser):
    # Add custom fields here
    # Example:
    # bio = models.TextField(blank=True)

    def __str__(self):
        return self.username