# coding=UTF-8
"""
TuxieMagick 0.5
    by Alvaro Mouriño ( http://tuxie.debianuruguay.org )
GPLv3 ( http://www.gnu.org/licenses/gpl-3.0.html )
"""
from os import path


class Image:
    def __init__(self, filename):
        self.x, self.y = 0, 0
        self.actions = []
        if path.exists(filename):
            self.exists = True
        else:
            self.exists = False
            # print filename
        self.filename = filename

    def size(self):
        return Dimension(self)

    def scale(self, width, height=None):
        self.x = width
        if height:
            self.y = height
        self.actions.append('scale')

    def crop(self, size, gravity='center'):
        self.crop = size
        self.crop_gravity = gravity
        self.actions.append('crop')

    def write(self, filename=None):
        import os

        error = 0
        params = ''
        if self.y:
            params = 'x%i' % self.y
        if not filename:
            filename = self.filename
        if not self.actions:
            source = open(self.filename, 'r')
            destination = open(filename, 'w')
            destination.write(source.read())
            return True
        for action in self.actions:
            if action == 'scale':
                binary = 'convert'
                command = '%(binary)s %(input)s -%(action)s ' \
                          '%(width)s%(height)s %(output)s' % \
                    {'binary': binary,
                     'input': self.filename,
                     'action': action,
                     'width': self.x,
                     'height': params,
                     'output': filename}
            elif action == 'watermark':
                binary = 'composite'
                command = '%(binary)s -%(action)s %(brightness)s -gravity ' \
                          '%(gravity)s %(watermark)s %(input)s %(output)s' % \
                    {'binary': binary,
                     'action': action,
                     'brightness': self.brightness,
                     'gravity': self.gravity,
                     'watermark': self.watermark,
                     'input': self.filename,
                     'output': filename}
            elif action == 'comment':
                binary = 'convert'
                command = '%(binary)s -%(action)s "%(comment)s" ' \
                          '%(input)s %(output)s' % \
                    {'binary': binary,
                     'action': action,
                     'comment': self.comment,
                     'input': self.filename,
                     'output': filename}
            elif action == 'crop':
                binary = 'convert'
                command = '%(binary)s -%(action)s %(size)s ' \
                          '%(input)s %(output)s' % \
                    {'binary': binary,
                     'action': action,
                     'size': self.crop,
                     'input': self.filename,
                     'output': filename}
            print command + '\n'
            if os.system(command) != 0:
                return False
            self.filename = filename
        return True

    def watermark(self, watermark, brightness='13.0', gravity='southeast'):
        self.brightness = brightness
        self.watermark = watermark
        self.gravity = gravity
        self.actions.append('watermark')

    def comment(self, comment):
        self.comment = comment
        self.actions.append('comment')


class Dimension:
    def __init__(self, image):
        import commands
        if image.exists:
            image.x = int(commands.getoutput('identify -format %%w %s' %
                image.filename))
            image.y = int(commands.getoutput('identify -format %%h %s' %
                image.filename))
        else:
            image.x, image.y = 0, 0
        self.image = image

    def __str__(self):
        return "%ix%i" % (self.image.x, self.image.y)

    def width(self):
        return self.image.x

    def height(self):
        return self.image.y

# class ImageNotFoundError(Exception):
#     pass
