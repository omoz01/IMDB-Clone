from rest_framework import serializers
from films.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('watchlist',)
        
 
class WatchListSerializer(serializers.ModelSerializer):
    platform =serializers.CharField(source='platform.name')
    # reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = WatchList
        fields = "__all__"
        
        
    len_title = serializers.SerializerMethodField()
    
    def get_len_title(self, object):
        length = len(object.title)
        return length
        


    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name is to short")
        else:
            return value
        
    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("Title and storyline should not be the samething!")
        else:
            return data
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"
