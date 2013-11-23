# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Standard Image Field - This code belongs to the stdimage project located
in http://github.com/humanfromearth/django-stdimage. The original project
is not ported for Python 3 and gives errors during imports so I've been forced
to include an all-in-one version of the project here.
"""

import os, shutil

from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.widgets import AdminFileWidget
from django.db.models import signals
from django.db.models.fields.files import ImageField, ImageFileDescriptor
from django.forms.fields import ImageField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class StdImageFormField(ImageField):
    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(StdImageFormField, self).clean(data, initial)
        else:
            return '__deleted__'


class DelAdminFileWidget(AdminFileWidget):
    """An AdminFileWidget that shows a delete checkbox"""
    input_type = 'file'

    def render(self, name, value, attrs=None):
        input = super(forms.widgets.FileInput, self).render(name, value, attrs)
        if value and hasattr(value, 'field'):
            return mark_safe(render_to_string('stdimage/admin_widget.html', {
                'name': name,
                'value': value,
                'input': input,
                'show_delete_button': value.field.blank,
                'MEDIA_URL': settings.MEDIA_URL,
            }))
        else:
            return mark_safe(input)

    def value_from_datadict(self, data, files, name):
        if not data.get('%s_delete' % name):
            return super(DelAdminFileWidget, self).\
                            value_from_datadict(data, files, name)
        else:
            return '__deleted__'


class ThumbnailField(object):
    """Instances of this class will be used to access data of the
    generated thumbnails

    """

    def __init__(self, name):
        self.name = name
        self.storage = FileSystemStorage()

    def path(self):
        return self.storage.path(self.name)

    def url(self):
        return self.storage.url(self.name)

    def size(self):
        return self.storage.size(self.name)


class StdImageFileDescriptor(ImageFileDescriptor):
    """ The thumbnail property of the field should be accessible in instance
    cases

    """
    def __set__(self, instance, value):
        super(StdImageFileDescriptor, self).__set__(instance, value)
        self.field._set_thumbnail(instance)


class StdImageField(ImageField):
    """Django field that behaves as ImageField, with some extra features like:
        - Auto resizing
        - Automatically generate thumbnails
        - Allow image deletion

    """
    #import ipdb;ipdb.set_trace()
    descriptor_class = StdImageFileDescriptor

    def __init__(self, *args, **kwargs):

        """Added fields:
            - size: a tuple containing width and height to resize image, and
            an optional boolean setting if is wanted forcing that size (None for not resizing).
                * Example: (640, 480, True) -> Will resize image to a width of
                640px and a height of 480px. File will be cutted if necessary
                for forcing te image to have the desired size
            - thumbnail_size: a tuple with same values than `size'
            (None for not creating a thumbnail

        """
        size = kwargs.pop('size', None)
        thumbnail_size = kwargs.pop('thumbnail_size', None)

        params_size = ('width', 'height', 'force')
        for att_name, att in (('size', size),
                              ('thumbnail_size', thumbnail_size)):
            if att and isinstance(att, (tuple, list)):
                setattr(self, att_name, dict(map(None, params_size, att)))
            else:
                setattr(self, att_name, None)
        super(StdImageField, self).__init__(*args, **kwargs)

    def _get_thumbnail_filename(self, filename):
        """Returns the thumbnail name associated to the standard image filename

        Example::

            ./myproject/media/img/picture_1.jpeg

        returns::

            ./myproject/media/img/picture_1.thumbnail.jpeg

        """
        splitted_filename = list(os.path.splitext(filename))
        splitted_filename.insert(1, '.thumbnail')
        return ''.join(splitted_filename)

    def _resize_image(self, filename, size):
        """Resizes the image to specified width, height and force option

        Arguments::

        filename -- full path of image to resize
        size -- dictionary with
            - width: int
            - height: int
            - force: bool
                if True, image will be cropped to fit the exact size,
                if False, it will have the bigger size that fits the specified
                size, but without cropping, so it could be smaller on width
                or height

        """

        WIDTH, HEIGHT = 0, 1
        try:
            import Image, ImageOps
        except ImportError:
            from PIL import Image, ImageOps
        img = Image.open(filename)
        if (img.size[WIDTH] > size['width'] or
            img.size[HEIGHT] > size['height']):

            #If the image is big resize it with the cheapest resize algorithm
            factor = 1
            while (img.size[0]/factor > 2*size['width'] and
                   img.size[1]*2/factor > 2*size['height']):
                factor *=2
            if factor > 1:
                img.thumbnail((int(img.size[0]/factor),
                               int(img.size[1]/factor)), Image.NEAREST)

            if size['force']:
                img = ImageOps.fit(img, (size['width'], size['height']),
                                   Image.ANTIALIAS)
            else:
                img.thumbnail((size['width'], size['height']), Image.ANTIALIAS)
            try:
                img.save(filename, optimize=1)
            except IOError:
                img.save(filename)

    def _rename_resize_image(self, instance=None, **kwargs):
        """Renames the image, and calls methods to resize and create the
        thumbnail.

        """

        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path
            ext = os.path.splitext(filename)[1].lower().replace('jpg', 'jpeg')
            dst = self.generate_filename(instance, '%s_%s%s' % (self.name,
                                                instance._get_pk_val(), ext))
            dst_fullpath = os.path.join(settings.MEDIA_ROOT, dst)
            if os.path.abspath(filename) != os.path.abspath(dst_fullpath):
                os.rename(filename, dst_fullpath)
                if self.size:
                    self._resize_image(dst_fullpath, self.size)
                if self.thumbnail_size:
                    thumbnail_filename = self._get_thumbnail_filename(
                        dst_fullpath)
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
            filename = self.generate_filename(instance,
                        os.path.basename(getattr(instance, self.name).path))
            thumbnail_filename = self._get_thumbnail_filename(filename)
            thumbnail_field = ThumbnailField(thumbnail_filename)
            setattr(getattr(instance, self.name), 'thumbnail', thumbnail_field)


    def formfield(self, **kwargs):
        """Specify form field and widget to be used on the forms"""

        kwargs['widget'] = DelAdminFileWidget
        kwargs['form_class'] = StdImageFormField
        return super(StdImageField, self).formfield(**kwargs)

    def save_form_data(self, instance, data):
        """Overwrite save_form_data to delete images if "delete" checkbox
        is selected

        """
        if data == '__deleted__':
            filename = getattr(instance, self.name).path
            if os.path.exists(filename):
                os.remove(filename)
            thumbnail_filename = self._get_thumbnail_filename(filename)
            if os.path.exists(thumbnail_filename):
                os.remove(thumbnail_filename)
            setattr(instance, self.name, None)
        else:
            super(StdImageField, self).save_form_data(instance, data)

    def get_db_prep_save(self, value, connection=None):
        """Overwrite get_db_prep_save to allow saving nothing to the database
        if image has been deleted

        """

        if value:
            return super(StdImageField, self).get_db_prep_save(value, connection=connection)
        else:
            return u''

    def contribute_to_class(self, cls, name):
        """Call methods for generating all operations on specified signals"""

        super(StdImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._rename_resize_image, sender=cls)
        signals.post_init.connect(self._set_thumbnail, sender=cls)
