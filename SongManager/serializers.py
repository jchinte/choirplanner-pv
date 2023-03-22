from SongManager.models import Composer, Tag, Song, SongFile, FileType

from rest_framework import serializers

class ComposerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composer
        fields = ['id', 'first_name', 'last_name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name']

class SongFileListingField(serializers.RelatedField):
    def to_representation(self, value):
        url = value.file.url
        return url

class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = ['id', 'type']

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class SongFileSerializer(serializers.ModelSerializer):
    filetypes = FileTypeSerializer(many=True, required=False)

    def to_representation(self, value):
        
        if value.thumbnail:
            self.context['thumbnail'] = value.thumbnail
        return super().to_representation(value)

    def create(self, validated_data):
        filetypes = None
        if 'filetypes' in validated_data:
            filetypes = validated_data.pop('filetypes')
        songfile = SongFile.objects.create(**validated_data)
        if filetypes:
            add_all(filetypes, songfile, FileType, 'filetypes')
        return songfile

    def update(self, instance, validated_data, *args, **kwargs):
        if 'filetypes' in validated_data:
            filetypes = validated_data.pop('filetypes')
            add_all(filetypes, instance, FileType, 'filetypes')
        return super().update(instance, validated_data)
    class Meta:
        model = SongFile
        fields = ['id', 'file', 'song', 'comments', 'filetypes', 'thumbnail']

def add_all(collection, obj, Cls, attr):
    getattr(obj, attr).clear()
    for item_data in collection:
        item, created = Cls.objects.get_or_create(**item_data)
        getattr(obj, attr).add(item)

class SongListSerializer(DynamicFieldsModelSerializer):
    composers = ComposerSerializer(required=True, many=True)
    tags = TagSerializer(required=False, many=True)
    #files = SongFileSerializer(many=True, read_only=True, required=False)
    #files = SongFileListingField(many=True, read_only=True)
    class Meta:
        model = Song
        fields = ['id', 'title', 'composers', 'tags', 'first_line',]
class SongSerializer(DynamicFieldsModelSerializer):
    composers = ComposerSerializer(required=False, many=True)
    tags = TagSerializer(required=False, many=True)
    files = SongFileSerializer(many=True, read_only=True, required=False)
    #files = SongFileListingField(many=True, read_only=True)
    class Meta:
        model = Song
        fields = ['id', 'title', 'composers', 'tags', 'first_line', 'files']

    def create(self, validated_data):
        print("In create")
        composers_data = validated_data.pop('composers') if 'composers' in validated_data else None
        tags_data = validated_data.pop('tags') if 'tags' in validated_data else None
        song = Song.objects.create(**validated_data)

        if composers_data:
            add_all(composers_data, song, Composer, 'composers')
        if tags_data:
            add_all(tags_data, song, Tag, 'tags')

        return song



    def update(self, instance, validated_data):
        if 'composers' in validated_data:
            composers_data = validated_data.pop('composers')
            instance.composers.clear()
            add_all(composers_data, instance, Composer, 'composers')
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')       
            instance.tags.clear()
            add_all(tags_data, instance, Tag, 'tags')
        return super().update(instance, validated_data)
"""

tests

from SongManager.models import Song
from SongManager.serializers import SongSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
song = Song.objects.get(id=653)

serializer = SongSerializer(song)
print(serializer.data)
print(JSONRenderer().render(serializer.data))


"""