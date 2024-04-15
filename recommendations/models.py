from django.db import models

class Rating(models.Model):
    user_id = models.IntegerField()
    item_id = models.IntegerField()  # Assuming this corresponds to the movie ID
    rating = models.FloatField()

    def __str__(self):
        return f"User {self.user_id} rated movie {self.item_id} with {self.rating} stars."

class Movie(models.Model):
    item_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
