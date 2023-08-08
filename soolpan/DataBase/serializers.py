from  rest_framework import serializers
from .models import Tal, Comment

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tal
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'