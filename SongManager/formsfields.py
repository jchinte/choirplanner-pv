from __future__ import unicode_literals
from SongManager.models import SongFile, Song, Composer, Tag
from django.forms import Field, Form, ModelForm, HiddenInput, TextInput, CharField, ChoiceField
import collections
from django.utils.encoding import smart_str
from SongManager.models import FileType

#Fields

class MultiDataField(CharField):
    def to_python(self, value):
        try:
            return list(filter(lambda s: s, map(lambda s: s.strip(), smart_str(value).split(';'))))
        except:
            if isinstance(value, collections.Iterable):
                return self.to_strings(value)
            else:
                return value
    
    def to_strings(self, values):
        return [str(value).strip() for value in values if str(value).strip()]

    def validate(self, value):
        super(MultiDataField, self).validate(value)

def split_name(name):
    #case last, first       
    if "," in name:
        composer_names = name.split(',', 1)
        return composer_names[1].strip(), composer_names[0].strip()

    #case first last
    composer_names = name.rsplit(' ', 1)
    if len(composer_names) == 1:
        return '', composer_names[0].strip()
    return composer_names[0].strip(), composer_names[1].strip()

class MultiNameField(MultiDataField):

    def to_python(self, value):
        new_value = super(MultiNameField, self).to_python(value)
        return [list(split_name(name)) for name in new_value]
    
#Forms



def inline_list(object_list):
    return ';'.join([str(name) for name in object_list])

class SongForm(ModelForm):
    composer_list = MultiDataField(label='composers')
    tag_list = MultiDataField(label='tags')

    def __init__(self, *args, **kargs):
        if 'initial' not in kargs:
            kargs['initial'] = {}

        #initialize composer and tag text fields from given instance
        if 'instance' in kargs:
            instance = kargs['instance']
            if instance is not None:
                kargs['initial'].update({
                                         'composer_list': inline_list(instance.composers.all()),
                                         'tag_list' : inline_list(instance.tags.all()),
                                         })
            
        super(SongForm, self).__init__(*args, **kargs)
    class Meta:
        model = Song
        fields = ('title',
                  'composer_list',
                  'tag_list',
                  'first_line',)
    def save(self):
        ### save form
        # call super
        instance = super(SongForm, self).save()
        
        ###add many to many fields
        #add composers
        instance.composers.clear()
        for composer_name in self.cleaned_data['composer_list']:
            first, last = split_name(composer_name)
            c, created = Composer.objects.get_or_create(first_name=first, last_name=last)
            instance.composers.add(c)
        
        #add tags
        instance.tags.clear()
        for tag_name in self.cleaned_data['tag_list']:
            t, created = Tag.objects.get_or_create(tag_name=tag_name)
            instance.tags.add(t)

        return instance
    
class SearchForm(Form):
    SEARCH_CHOICES = (
        ('A', 'everything'),
        ('B', 'titles'),
        ('C', 'tags'),
        ('D', 'composer'),
        ('E', 'first line lyrics')
    )
    search = CharField(max_length=200)
    options = ChoiceField(choices=SEARCH_CHOICES)
    
class SongFileForm(ModelForm):
    filetype_list = MultiDataField(max_length=100, label='File Types', required=False)
    def __init__(self, *args, **kargs):
        if 'initial' not in kargs:
            kargs['initial'] = {}

        #initialize composer and tag text fields from given instance
        if 'instance' in kargs:
            instance = kargs['instance']
            if instance is not None:
                kargs['initial'].update({
                                         'filetype_list': inline_list(instance.filetypes.all()),
                                         })
            
        super(SongFileForm, self).__init__(*args, **kargs)
    
    class Meta:
        model = SongFile
        fields = ('file', 'song')
        widgets = {
                   'song' : HiddenInput
        }
    def save(self):
        ### save form
        # call super
        instance = super(SongFileForm, self).save()
        
        ###add many to many fields
       
        #add file types
        instance.filetypes.clear()
        for filetype_name in self.cleaned_data['filetype_list']:
            f, created = FileType.objects.get_or_create(type=filetype_name)
            instance.filetypes.add(f)

        return instance        
