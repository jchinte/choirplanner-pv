"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from SongManager.models import Song, Composer, Tag, SongFile
from SongManager.serializers import SongSerializer, SongFileSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from music_planner0 import settings
import io, os
from collections import OrderedDict


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class SongSerializerTest(TestCase):
    def setUp(self):
        serializer = SongSerializer(data=JSONParser().parse(io.BytesIO(b'{"title":"Anima Christi","composers":[{"first_name":"Jandi","last_name":"Arboleda"}],"tags":[{"tag_name":"SATB"},{"tag_name":"Bukas Palad"}],"first_line":"Soul of Christ, sanctify me"}')))
        print(serializer.is_valid(), serializer.errors)
        serializer.save()
        print(Tag.objects.all())
        pass
    def test_create(self):
        #serializer = SongSerializer(data=JSONParser().parse(io.BytesIO(b'{"title":"Anima Christi","composers":[{"first_name":"Jandi","last_name":"Arboleda"}],"tags":[{"tag_name":"SATB"},{"tag_name":"Bukas Palad"}],"first_line":"Soul of Christ, sanctify me"}')))
        #serializer.save()
        song = Song.objects.get(title="Anima Christi")
        self.assertIsNotNone(song)
        self.assertListEqual(list(song.composers.all()), list(Composer.objects.filter(song__id=song.id)))
        song.composers

    def test_serialize_song(self):
        song = Song.objects.get(title="Anima Christi")
        serializer = SongSerializer(song)
        song_json = JSONRenderer().render(serializer.data)
        print(song_json)
        test_str = b'{"id":2,"title":"Anima Christi","composers":[{"id":2,"first_name":"Jandi","last_name":"Arboleda"}],"tags":[{"id":3,"tag_name":"SATB"},{"id":4,"tag_name":"Bukas Palad"}],"first_line":"Soul of Christ, sanctify me","files":[]}'
        print(test_str)
        self.assertJSONEqual(song_json, serializer.data)
        
    def test_update_song(self):
        song = Song.objects.get(title="Anima Christi")
        serializer = SongSerializer(song)
        serializer.update(song, {"first_line": "NOTHING"})
        song2 = Song.objects.get(title="Anima Christi")
        self.assertEqual(str(song2.first_line), "NOTHING")

    # def test_upload_song(self):
    #     song = Song.objects.get(title="Anima Christi")
    #     c = Client()

    #     with open(os.path.join(settings.BASE_DIR, 'wsgi.py')) as fp:
    #         fts = [{"type","py"}, {"type","code"}]
    #         print("fts: {0}".format(fts))
    #         res = c.post('/songs/api/upload/', {"song": song.id, "comments":"this is a comment", "filetypes":fts, "file": fp})
    #         print(res)
    #         print(res.content)
    #     song = Song.objects.get(title="Anima Christi")
    #     serializer = SongSerializer(song)
    #     print(serializer.data)
    #     print(SongFile.objects.all())
    #     print(Song.objects.all())

    #     serializer = SongFileSerializer(SongFile.objects.get(song=song.id))
    #     serializer.update(SongFile.objects.get(song=song.id), {"filetypes":[{"type":"py"}, {"type":"code"}]})
    #     song = Song.objects.get(title="Anima Christi")
    #     serializer = SongSerializer(song)
    #     print(serializer.data)
        
    #     #other checks