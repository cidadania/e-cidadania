# coding=UTF-8
from django.template import Library, Node, Template, TemplateSyntaxError, \
    Variable
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as u_
from django.contrib.auth.models import User
from django.conf import settings

from userprofile import profile_settings as _settings
from userprofile.models import Profile
# from PythonMagick import Image
from utils.TuxieMagick import Image

from os import path, makedirs
from shutil import copy

register = Library()


class ResizedThumbnailNode(Node):
    def __init__(self, size, username=None):
        try:
            self.size = int(size)
        except:
            self.size = Variable(size)
        self.user = username

    def get_user(self, context):
        # If there's a username, go get it! Otherwise get the current.
        if self.user:
            try:
                user = User.objects.get(username=self.user)
            except:
                user = Variable(self.user).resolve(context)
        else:
            user = Variable('user').resolve(context)
        return user

    def size_equals(self, file=None):
        if not file:
            return self.size == _settings.DEFAULT_AVATAR_WIDTH
        else:
            return self.size == Image(file).size().width()

    def get_profile(self):
        # Maybe django-profile it's not set as AUTH_PROFILE_MODULE
        try:
            profile = self.user.get_profile()
        except Exception, e:
            print e
            if self.user.is_authenticated():
                profile = Profile.objects.get(user=self.user)
            else:
                print "There is no user to get it's avatars for."
                return ''
        return profile

    def get_file(self, profile=None):
        # For compatibility with the official django-profile model I check
        # whether it's a path or just a filename.
        # In my opinion in the database should only be saved the file name,
        # and all files be stored in a standard directory:
        # settings.AVATAR_DIRS[int]/str(User)/settings_DEFAULT_AVATAR_WIDTH/
        default = False
        try:
            file_root = path.join(settings.MEDIA_ROOT,
                profile.avatar[:profile.avatar.rindex('/') +1])
            file_name = profile.avatar[profile.avatar.rindex('/') +1:]
        except:
            file_root = _settings.AVATARS_DIR
            if profile is not None and profile.avatar:
                file_root = path.join(file_root, self.size)
                file_name = profile.avatar
            else:
                file_name = _settings.DEFAULT_AVATAR
                default = True
        return (file_root, file_name, default)

    def as_url(self, path):
        try:
            return path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
        except:
            return ''

    def render(self, context):
        try:
            # If size is not an int, then it's a Variable, so try to resolve it.
            if not isinstance(self.size, int):
                self.size = int(self.size.resolve(context))
            self.user = self.get_user(context)
        except Exception, e:
            print e
            return ''  # just die...
        if self.size > _settings.DEFAULT_AVATAR_WIDTH:
            return ''  # unacceptable
        profile = self.get_profile()
        if not profile:
            return ''
        # Avatar's heaven, where all the avatars go.
        avatars_root = path.join(_settings.AVATARS_DIR,
                                 slugify(self.user.username))
        file_root, file_name, defaulting = self.get_file(profile)
        if defaulting:
            file_root = _settings.AVATARS_DIR
            if self.size_equals():
                return self.as_url(path.join(file_root, file_name))
        file_path = path.join(file_root, file_name)
        # I don't return the default because I have to resize it.
        if not defaulting:
            if path.exists(file_path) and self.size_equals(file_path):
                return self.as_url(file_path)
            else:
                if not profile.avatar:
                    file_root = _settings.AVATARS_DIR
                    file_path = path.join(file_root, _settings.DEFAULT_AVATAR)
        # Oops, I din't find it, let's try to generate it.
        if path.exists(file_path):
            orig_file = Image(file_path)
            dest_root = path.join(avatars_root, str(self.size))
            try:
                makedirs(dest_root)
            except Exception, e:
                print e
            # Save the new path for later...
            dest_path = path.join(dest_root, file_name)
        else:
            # Did my best...
            return ''  # fail silently
        orig_file.scale(self.size)
        if orig_file.write(dest_path):
            return self.as_url(dest_path)
        else:
            print '=== ERROR ==='
            return ''  # damn! Close but no cigar...


@register.tag('avatar')
def Thumbnail(parser, token):
    bits = token.contents.split()
    username = None
    if len(bits) > 3:
        raise TemplateSyntaxError(u_(u"You have to provide only the size as \
            an integer (both sides will be equal) and optionally, the \
            username."))
    elif len(bits) == 3:
        username = bits[2]
    elif len(bits) < 2:
        bits.append(_settings.DEFAULT_AVATAR_WIDTH)
    return ResizedThumbnailNode(bits[1], username)
