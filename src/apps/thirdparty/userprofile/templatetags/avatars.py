# coding=UTF-8
from django.template import Library, Node, Template, TemplateSyntaxError, \
    Variable
from django.utils.translation import ugettext as _
from apps.thirdparty.userprofile.models import Avatar, AVATAR_SIZES
from django.contrib.auth.models import User
from django.conf import settings
import Image
# from PythonMagick import Image
# from utils.TuxieMagick import Image
import os
import time

register = Library()

if hasattr(settings, "DEFAULT_AVATAR") and settings.DEFAULT_AVATAR:
    DEFAULT_AVATAR = settings.DEFAULT_AVATAR
else:
    DEFAULT_AVATAR = os.path.join(settings.MEDIA_ROOT, "generic.jpg")


class ResizedThumbnailNode(Node):
    def __init__(self, size, username=None):
        try:
            self.size = int(size)
        except:
            self.size = Variable(size)
        if username:
            self.user = Variable(username)
        else:
            self.user = Variable("user")

    def render(self, context):
        # If size is not an int, then it's a Variable, so try to resolve it.
        if not isinstance(self.size, int):
            self.size = int(self.size.resolve(context))

        if not self.size in AVATAR_SIZES:
            return ''

        try:
            user = self.user.resolve(context)
            avatar = Avatar.objects.get(user=user, valid=True).image
            avatar_path = avatar.path
            base, filename = os.path.split(avatar_path)
            name, extension = os.path.splitext(filename)
            filename = os.path.join(base, "%s.%s%s" % (name, self.size, extension))
            base, temp = os.path.split(avatar.url)
            url = os.path.join(base, "%s.%s%s" % (name, self.size, extension))
        except:
            avatar_path = DEFAULT_AVATAR
            base, filename = os.path.split(avatar_path)
            generic, extension = os.path.splitext(filename)
            filename = os.path.join(base, "%s.%s%s" % (generic, self.size, extension))
            url = filename.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)

        if not os.path.isfile(filename):
            image = Image.open(avatar_path)
            image.thumbnail((self.size, self.size), Image.ANTIALIAS)
            image.save(filename, "JPEG")

        return url


@register.tag('avatar')
def Thumbnail(parser, token):
    bits = token.contents.split()
    username = None
    if len(bits) > 3:
        raise TemplateSyntaxError(_(u"You have to provide only the size as \
            an integer (both sides will be equal) and optionally, the \
            username."))
    elif len(bits) == 3:
        username = bits[2]
    elif len(bits) < 2:
        bits.append("96")
    return ResizedThumbnailNode(bits[1], username)
