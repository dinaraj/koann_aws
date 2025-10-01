import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path, prefix=''):
        self.path = sub_path
        self.prefix = prefix

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string + prefix
        filename = self.prefix + '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)
