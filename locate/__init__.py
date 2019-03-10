# -*- coding: utf-8 -*-
"""
/***************************************************************************
 locate
                                 A QGIS plugin
 locate
                             -------------------
        begin                : 2017-07-17
        copyright            : (C) 2017 by song
        email                : teemo91256@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load locate class from file locate.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .locate import locate
    return locate(iface)
