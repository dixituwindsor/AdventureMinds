
from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    def __str__(self):
        return 'pk=' +str (self.pk)+', name='+self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=True, primary_key=True, default=None)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    interested_places = models.ManyToManyField(Place, blank=True)
    preferences = models.ForeignKey('UserPreferences', on_delete=models.SET_NULL, null=True, blank=True)
    total_reviews = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

    def total_reviews(self):
        return self.review_set.count()


class PreferenceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PreferenceChoice(models.Model):
    category = models.ForeignKey(PreferenceCategory, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name}: {self.value}"


class UserPreferences(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_profile', null=True, blank=True)
    preferences = models.ManyToManyField(PreferenceChoice)

    def __str__(self):
        if self.user_profile:
            return f"Preferences for {self.user_profile.user.username}"
        else:
            return "No associated user profile"

    def get_selected_preferences(self):
        return [preference.value for preference in self.preferences.all()]

class TripPreference(models.Model):
    preferences = models.ManyToManyField(PreferenceChoice)


class ChatGroups(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(UserProfile, related_name='chat_groups')

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    chat_group = models.ForeignKey(ChatGroups, on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username if self.recipient else self.chat_group.name}: {self.content}"


class Trip(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    start_date = models.DateField(default=None, null=True)
    end_date = models.DateField(default=None, null=True)
    description = models.TextField(null=True, blank=True)
    preferences = models.ForeignKey('TripPreference', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.uploader_id}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id), self.user.first_name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=(('1','1 star'),('b','2 star'),('c', '3 star'),('d', '4 star'),('e', '5 star')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')

    def __str__(self):
        return f"{self.user}'s {self.rating}- star rating for {self.place}"

# class Post(models.Model):
#     place = models.ForeignKey(Place, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title



# class UserProfile(User):
#     interested_places = models.ManyToManyField(Place)
#     total_reviews = models.PositiveIntegerField(default=0)
#     total_ratings = models.PositiveIntegerField(default=0)
#     average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
#     def __str__(self):
#         return self.get_username()
#
#     def total_reviews(self):
#         return self.review_set.count()
#
#     def average_rating(self):
#         if self.total_reviews() > 0:
#             return self.review_set.all().aggregate(models.Avg('rating'))['rating__avg']
#         return 0
