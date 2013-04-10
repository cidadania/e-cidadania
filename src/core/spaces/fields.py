# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 Cidadania S. Coop. Galega
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
from django.db.models.fields.files import ImageField
from django.db.models import signals
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class ThumbnailField:
    """Instances of this class will be used to access data of the
    generated thumbnails"""
    def __init__(self, name):
        self.name = name
        self.storage = FileSystemStorage()

    def path(self):
        return self.storage.path(self.name)

    def url(self):
        return self.storage.url(self.name)

    def size(self):
        return self.storage.size(self.name)


class StdImageField(ImageField):
    """Django field that behaves as ImageField, with some extra features like:
        - Auto resizing
        - Automatically generate thumbnails
    """
    def __init__(self, verbose_name=None, name=None, width_field=None,
                 height_field=None, size=None, thumbnail_size=None, **kwargs):
        """Added fields:
            - size: a tuple containing width and height to resize image, and
                an optional boolean setting if is wanted forcing that size
                (None for not resizing).
            - thumbnail_size: a tuple with same values than `size' (None for
                not creating a thumbnail
        Example: (640, 480, True) -> Will resize image to a width of 640px and
            a height of 480px. File will be cutted if necessary for forcing
            the image to have the desired size
        """
        params_size = ('width', 'height', 'force')
        extra_args = dict(size=size, thumbnail_size=thumbnail_size)
        for att_name, att in extra_args.items():
            if att and (isinstance(att, tuple) or isinstance(att, list)):
                setattr(self, att_name, dict(map(None, params_size, att)))
            else:
                setattr(self, att_name, None)
        super(StdImageField, self).__init__(verbose_name, name, width_field,
            height_field, **kwargs)

    def contribute_to_class(self, cls, name):
        """Call methods for generating all operations on specified signals
        """
        super(StdImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._rename_resize_image, sender=cls)
        signals.post_init.connect(self._set_thumbnail, sender=cls)

    def _get_thumbnail_filename(self, filename):
        """Returns the thumbnail name associated to the standard image filename

        Example: /var/www/myproject/media/img/picture_1.jpeg will return
            /var/www/myproject/media/img/picture_1.thumbnail.jpeg
        """
        splitted_filename = list(os.path.splitext(filename))
        splitted_filename.insert(1, '.thumbnail')
        return ''.join(splitted_filename)

    def _resize_image(self, filename, size):
        """Resizes the image to specified width, height and force option
            - filename: full path of image to resize
            - size: dictionary containing:
                - width: new width
                - height: new height
                - force: if True, image will be cropped to fit the exact size,
                    if False, it will have the bigger size that fits the
                    specified size, but without cropping, so it could be
                    smaller on width or height
        """
        WIDTH, HEIGHT = 0, 1
        from PIL import Image, ImageOps
        img = Image.open(filename)
        if img.size[WIDTH] > size['width'] or img.size[HEIGHT] > size['height']:
            if size['force']:
                img = ImageOps.fit(img, (size['width'], size['height']), Image.ANTIALIAS)
            else:
                img.thumbnail((size['width'], size['height']), Image.ANTIALIAS)
            try:
                img.save(filename, optimize=1)
            except IOError:
                img.save(filename)

    def _rename_resize_image(self, instance=None, **kwargs):
        """Renames the image, and calls methods to resize and create the
            thumbnail
        """
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path
            ext = os.path.splitext(filename)[1].lower().replace('jpg', 'jpeg')
            dst = self.generate_filename(instance, '%s_%s%s' % (
                self.name,
                instance._get_pk_val(),
                ext))
            dst_fullpath = os.path.join(settings.MEDIA_ROOT, dst)
            normpath = lambda x: os.path.normpath(os.path.abspath(x))
            if normpath(filename) != normpath(dst_fullpath):
                os.rename(filename, dst_fullpath)
                if self.size:
                    self._resize_image(dst_fullpath, self.size)
                if self.thumbnail_size:
                    thumbnail_filename = self._get_thumbnail_filename(dst_fullpath)
                    shutil.copyfile(dst_fullpath, thumbnail_filename)
                    self._resize_image(thumbnail_filename, self.thumbnail_size)
                setattr(instance, self.attname, dst)
                instance.save()

    def _set_thumbnail(self, instance=None, **kwargs):
        """Creates a "thumbnail" object as attribute of the ImageField instance
        Thumbnail attribute will be of the same class of original image, so
        "path", "url"... properties can be used
        """
        if getattr(instance, self.name):
            filename = self.generate_filename(
                instance,
                os.path.basename(
                    getattr(instance, self.name).path))
            thumbnail_filename = self._get_thumbnail_filename(filename)
            thumbnail_field = ThumbnailField(thumbnail_filename)
            setattr(getattr(instance, self.name), 'thumbnail', thumbnail_field)
