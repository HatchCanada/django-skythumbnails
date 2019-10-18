# -*- coding: utf-8 -*-
#
#  This file is part of django-sky-thumbnails.
#
#  django-sky-thumbnails adds thumbnail support to the default ImageField.
#
#  Copyright 2012 Concentric Sky, Inc. All Rights Reserved.
#  http://www.concentricsky.com
#  Written by: Kyle Rimkus [Mar 2012]
#  This code may not be used without permission.
#
#  Parts of this code are derivative of django-thumbnail-works.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-thumbnail-works
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-thumbnail-works
#
#  Copyright 2010 George Notaras <gnot [at] g-loaded.eu>

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None):
        output = []
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        if value and hasattr(value, 'field') and value.field and value.field.thumbnails:
            for thumbnail_name, thumbnail_attrs in value.field.thumbnails.items():
                output.append('<span class="thumbnail">%s: <a target="_blank" href="%s"><img src="%s"/></a></span>' % \
                    (thumbnail_name, getattr(value, thumbnail_name).url, getattr(value, thumbnail_name).url))
        return mark_safe(''.join(output))
