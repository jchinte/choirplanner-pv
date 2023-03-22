from Event_Planner.models import Activity, Event, LinkedSegment, Participant, Role, Segment, SongSegment
from rest_framework import serializers
from django.contrib.auth.models import User
from SongManager.serializers import SongSerializer, SongListSerializer
from SongManager.models import Song

class SegmentSerializer(serializers.ModelSerializer):
    #queryset = Segment.objects.select_subclasses()
    notes = serializers.CharField(max_length=100, required=False)
    order = serializers.IntegerField(required=False)

    def get_queryset(self):
        return Segment.objects.select_subclasses()
    def to_representation(self, instance):
        if isinstance(instance, SongSegment):
            return SongSegmentSerializer(instance=instance).data
        return super().to_representation(instance)

    def validate_song(self, value):
        if value is None:
            return value
        if isinstance(value, Song):
            return value
        return Song.objects.get(id=value)
    def to_internal_value(self, data):
        if data.get('song'):
            self.Meta.model = SongSegment
        else:
            self.Meta.model = Segment
        if not data.get('order'):
            event = data.get('event')
            data['order'] =  1+len(Segment.objects.filter(event=event))
        value =  super().to_internal_value(data)
        return value
    class Meta:
        model = Segment
        fields = '__all__'
    

class SongSegmentSerializer(serializers.ModelSerializer):
    song = SongListSerializer(required=False)
    class Meta:
        model = SongSegment
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True, required=False)
    class Meta:
        model = Event
        fields = '__all__'
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if getattr(instance, 'segments'):
            rep['segments'] = [SegmentSerializer(seg).data for seg in Segment.objects.filter(event=instance.id).select_subclasses()]
        return rep
    def to_internal_value(self, data):
        values =  super().to_internal_value(data)
        if 'segments' in data:
            for i in range(len(data['segments'])):
                values['segments'][i]['id'] = data['segments'][i]['id']
        if 'template' in data:
            values['template'] = int(data['template'])
        return values
    def create(self, validated_data):
        if 'template' in validated_data:
            template = validated_data.pop('template')
            event = super().create(validated_data)
            event.copy_event(int(template))
            return event
        return super().create(validated_data)
    def update(self, instance, validated_data):
        if 'segments' in validated_data:
            segments_data = validated_data.pop('segments')
            for segment_data in segments_data:
                if 'song' in segment_data and isinstance(segment_data['song'], Song):
                    segment_data['song'] = segment_data['song'].id 
                seg = Segment.objects.select_subclasses().get(id=segment_data['id'])
                seg_serializer = SegmentSerializer(seg, data=segment_data, partial=True)
                if seg_serializer.is_valid():
                    seg_serializer.save()
                else:
                    print("invalid!", seg_serializer.errors)

        return super().update(instance, validated_data)

class EventListSerializer(serializers.ModelSerializer):
    #segments = SegmentSerializer(many=True, required=False)
    class Meta:
        model = Event
        fields = ['id', 'date', 'title', 'is_template']
    #def to_representation(self, instance):
        # rep = super().to_representation(instance)
        # if getattr(instance, 'segments'):
        #     rep['segments'] = [SegmentSerializer(seg).data for seg in Segment.objects.filter(event=instance.id).select_subclasses()]
        # return rep