from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() # Muestra el nombre, no el ID
    category_id = serializers.PrimaryKeyRelatedField(
        source='category', queryset=Category.objects.all(), write_only=True
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'category_id')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"