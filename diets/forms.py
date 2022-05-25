"""Forms for the diets app"""
import datetime

from django import forms
from django.core import serializers
from django.forms import ValidationError, fields

from .models import (
    Day,
    Diet,
    Ingredient,
    IntermediaryDayMeal,
    IntermediaryMealIngredient,
    Meal,
)


class MealForm(forms.ModelForm):
    """Form for creating meals with searched and selected ingredients"""

    class Meta:
        """We don't include the author field since it will be mentioned in `save`"""

        model = Meal
        fields = ("name", "description", "recipe", "image")

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super(MealForm, self).__init__(*args, **kwargs)

    def verify_ingredients(self):
        """Verify that the ingredient data was correct"""
        ingr_data = self.data.get("ingredient_data")
        amounts = self.data.get("amounts")
        if not ingr_data or not amounts:
            raise ValidationError("Invalid ingredient data")
        try:
            ingr_arr = [
                Ingredient.objects.get(name=obj.object.name)
                for obj in serializers.deserialize("json", ingr_data)
            ]
            amounts_arr = [int(obj) for obj in amounts.split(",")]
            assert len(ingr_arr) == len(amounts_arr)
        except:
            raise ValidationError("Incoherent ingredient data")
        return ingr_arr, amounts_arr

    def clean(self):
        """Clean ingredients and amounts to the cleaned data"""
        ingredient_data, amounts = self.verify_ingredients()
        clean_data = self.cleaned_data
        clean_data["ingredients"] = ingredient_data
        clean_data["amounts"] = amounts
        return clean_data

    def save(self):
        """Save data with additional and create ingredient relations"""
        clean_data = self.cleaned_data
        my_meal = Meal.objects.create(
            name=clean_data["name"],
            description=clean_data["description"],
            recipe=clean_data["recipe"],
            image=clean_data["image"],
            author=self.author,
        )
        my_meal.save()
        for k in range(len(clean_data["ingredients"])):
            IntermediaryMealIngredient.objects.create(
                meal=my_meal,
                ingredient=clean_data["ingredients"][k],
                amount=clean_data["amounts"][k],
            )


class DietCreateForm(forms.ModelForm):
    """A form to create a diet (grab and backup days from a user)"""

    class Meta:
        """Don't include the auhtor as he will be added in the save() method"""

        model = Diet
        fields = ("name", "public", "description", "date")

    def save(self, author):
        """Save the diet and create the day backups & relations"""
        my_diet = Diet.objects.create(**self.cleaned_data, author=author)
        dates = [my_diet.date + datetime.timedelta(days=i) for i in range(8)]
        my_diet.save()
        for date in dates:
            instance, created = Day.objects.get_or_create(
                date=date, author=author, backup=False
            )
            if created:
                instance.backup = True
                instance.save()
            else:
                relations = IntermediaryDayMeal.objects.filter(day=instance)
                instance.pk = None
                instance.backup = True
                instance.save()  # generates a new instance
                for relation in relations:
                    relation.pk = None
                    relation.day = instance
                    relation.save()
            my_diet.days.add(instance)


class DietImportForm(forms.Form):
    """A form to import diets into your day"""

    date = fields.DateField()

    def clean(self):
        """Clean the slug and add it to the data"""
        slug = self.data.get("slug")
        if not slug:
            raise ValidationError("No slug")
        clean_data = self.cleaned_data
        clean_data["slug"] = slug
        return clean_data

    def save(self, author):
        """Fill the days of the user with the days from the selected diet"""
        clean_data = self.cleaned_data
        diet = Diet.objects.filter(slug=clean_data["slug"]).first()
        if not diet:
            raise ValidationError("No diet with that slug")

        for i in range(8):
            date = clean_data["date"] + datetime.timedelta(days=i)
            day = Day.objects.filter(date=date, author=author).first()
            if day:
                day.delete()

        for i, day in enumerate(diet.days.all()):
            relations = IntermediaryDayMeal.objects.filter(day=day)
            day.date = clean_data["date"] + datetime.timedelta(days=i)
            day.backup = False
            day.author = author
            day.save()
            for relation in relations:
                relation.day = day
                relation.save()