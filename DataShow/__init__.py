# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DataShow
                                 A QGIS plugin
 It's cool
                             -------------------
        begin                : 2017-07-12
        copyright            : (C) 2017 by CSMU
        email                : ol55432@yahoo.com.tw
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
    """Load DataShow class from file DataShow.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .data_show import DataShow
    return DataShow(iface)
