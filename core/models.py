from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):

    STATUS_CHOICES = (
        ('Lost', 'Lost'),
        ('Found', 'Found'),
        ('Claimed', 'Claimed'),
    )

    CATEGORY_CHOICES = (
        ('Phone', 'Phone'),
        ('Laptop', 'Laptop'),
        ('Bag', 'Bag'),
        ('ID Card', 'ID Card'),
        ('Keys', 'Keys'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', null=True, blank=True)

    item = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    date_lost = models.DateField()
    owner_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Status starts as Lost; only updated to Found/Claimed later
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Lost'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.status}] {self.item}"