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


VERSION = (1, 0, 1)


def get_version():
    version = '%d.%d.%d' % (VERSION[0], VERSION[1], VERSION[2])
    return version
