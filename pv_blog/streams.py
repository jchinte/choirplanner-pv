"""Streamfields live in here."""

from collections import OrderedDict
from wagtail.core import blocks
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.models import Filter, SourceImageIOError
from wagtail.images.api.fields import ImageRenditionField
# from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
import re
class ImageChooserBlockCustom(ImageChooserBlock):
    def __init__(self, *args, filter_spec='max-1920x1080', **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_spec = filter_spec
        
    def get_api_representation(self, value, context=None):
        self.filter_spec = context['filter_spec'] if 'filter_spec' in context else self.filter_spec
        s = super().get_api_representation(value, context)
        irf = ImageRenditionField(self.filter_spec)
        rep = irf.to_representation(value)
        return rep

class PageChooserBlockCustom(blocks.PageChooserBlock):
    def get_api_representation(self, value, context=None):
        print("page value: {0}".format(value))
        rep = super().get_api_representation(value, context)
        print("rep: {0}".format(rep))
        return {
            'id':value.id,
            'slug':value.slug,
        }

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""

    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:  # noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""

    title = blocks.CharBlock(required=True, help_text="Add your title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlockCustom(filter_spec='fill-300x200', required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", PageChooserBlockCustom(required=False)),
                (
                    "button_url",
                    blocks.URLBlock(
                        required=False,
                        help_text="If the button page above is selected, that will be used first.",  # noqa
                    ),
                ),
            ]
        )
    )

    class Meta:  # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff Cards"


class RichTextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""

    def get_api_representation(self, value, context=None):
        return richtext(value.source)

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichTextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features."""

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):  # noqa
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"

class YouTubeVideoBlock(blocks.CharBlock):
    """Richtext without (limited) all the features."""
    video_id = blocks.CharBlock(required=True, help_text="youtube video id")
    def __init__(
        self, required=True, help_text="Youtube Video ID", editor="default", features=None, **kwargs
    ):  # noqa
        super().__init__(**kwargs)
        
    def get_api_representation(self, value, context=None):
        return richtext(self.render_basic(value))
    class Meta:  # noqa
        template = "streams/youtube_block.html"
        icon = "placeholder"
        label = "YouTube Video"

class YouTubeVideoBlock2(blocks.StructBlock):
    """Richtext without (limited) all the features."""
    video_id = blocks.CharBlock(required=True, help_text="youtube video id")
    # def __init__(
    #     self, required=True, help_text="Youtube Video ID", editor="default", features=None, **kwargs
    # ):  # noqa
    #     super().__init__(**kwargs)
    def clean(self, value):
        errors={}
        if not value.get("video_id"):
            errors['video_id']=ErrorList(['You must enter a youtube video or an 11-character video ID'])
        else:
            pat = re.compile('embed\/([\w\d_-]{11})|v=([\w\d_-]{11})|youtu.be\/([\w\d_-]{11})|^([\w\d_-]{11})$')
            def find_val(lst):
                if not lst:
                    return None
                if lst[0]:
                    return lst[0]
                return find_val(lst[1:])
            m = pat.search(value['video_id'])
            if m:
                value["video_id"] = find_val(m.groups())
                return super().clean(value)
            else:
                errors['video_id']=ErrorList(['Enter a valid Youtube video or URL. Your entry is not valid'])
        raise ValidationError('Validation error in YouTubeVideoBlock2', params=errors)

    def get_api_representation(self, value, context=None):
        print(value, type(value))
        return richtext(self.render(value))
    class Meta:  # noqa
        template = "streams/youtube_block.html"
        icon = "media"
        label = "YouTube Video"


class CTABlock(blocks.StructBlock):
    """A simple call to action section."""

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=40)

    class Meta:  # noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"


class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls."""

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None

    # def latest_posts(self):
    #     return BlogDetailPage.objects.live()[:3]


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL."""

    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button page')

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
    #     return context

    class Meta:  # noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue