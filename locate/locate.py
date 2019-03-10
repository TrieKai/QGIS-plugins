# -*- coding: utf-8 -*-
"""
/***************************************************************************
 locate
                                 A QGIS plugin
 locate
                              -------------------
        begin                : 2017-07-17
        git sha              : $Format:%H$
        copyright            : (C) 2017 by song
        email                : teemo91256@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QTableWidget, QTableWidgetItem, QRadioButton
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from locate_dialog import locateDialog
from PyQt4 import QtGui
import os.path


class locate:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.dlg = locateDialog()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'locate_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&locate')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'locate')
        self.toolbar.setObjectName(u'locate')
        
        
        
        # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('locate', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = locateDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/locate/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'locate'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&locate'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
    
    
    def search_do(self):
        #取得選擇的layer
        global selectedLayer, selectedLayerIndex , layers
        layers = self.iface.legendInterface().layers()
        selectedLayerIndex = layer_combobox.currentIndex()
        selectedLayer = layers[selectedLayerIndex]
        
        fields = selectedLayer.pendingFields()
        fieldnames = [field.name() for field in fields]
        global attribute_data, select_data, select_id
        attribute_data = []
        select_data = []
        data = []
        global attribute_unicode
        attribute_unicode = []
        select_id = []
        #取得輸入的路名
        search_text = self.dlg.search_input.text()
        for feature in selectedLayer.getFeatures():
            attribute_unicode = ','.join(unicode(feature[x]) for x in fieldnames).replace("NULL", "")
            data = str(feature.id())+','+ attribute_unicode 
            splitData = data.split(',')
            attribute_data.append(splitData)
        #搜尋道路   
        for i in attribute_data:
            if i[3] == search_text:
                select_id.append(long(i[0]))
                select_data.append(i)
        self.locate_insert()
        #定位到輸入的所有道路
        if select_id != []:
            selectedLayer.setSelectedFeatures(select_id)
            self.iface.mapCanvas().zoomToSelected()
    
    
    def locate(self, selected):
        global selectedRadio_list
        selectedRadio_list = []
        #定位到選擇的巷弄
        if selected == True:
            for i in attribute_data:
                if i[3]+i[5]+i[6] == self.dlg.sender().text():
                    selectedRadio_list.append(long(i[0]))
        else:
            pass
        selectedLayer.setSelectedFeatures(selectedRadio_list)
        self.iface.mapCanvas().zoomToSelected()
                
    def locate_insert(self):
        print("locate")
        count = 0
        #清空formLayout
        for i in reversed(range(self.dlg.formLayout_3.count())): 
            self.dlg.formLayout_3.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.dlg.formLayout_4.count())): 
            self.dlg.formLayout_4.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.dlg.formLayout_5.count())): 
            self.dlg.formLayout_5.itemAt(i).widget().setParent(None)
        #將路名、巷、弄，合併展示    
        for i in select_data:
            if i[5] == "" and i[6] == "":
                samename = i[3]
            else:
                if count < 30 :
                    radioButton = QRadioButton(i[3]+i[5]+i[6])
                    self.dlg.formLayout_3.addRow(radioButton)
                    radioButton.toggled.connect(self.locate)
                elif count <=60 :
                    radioButton = QRadioButton(i[3]+i[5]+i[6])
                    self.dlg.formLayout_4.addRow(radioButton)
                    radioButton.toggled.connect(self.locate)
                else :
                    radioButton = QRadioButton(i[3]+i[5]+i[6])
                    self.dlg.formLayout_5.addRow(radioButton)
                    radioButton.toggled.connect(self.locate)
                count = count + 1    
                    
        
    def run(self):
        """Run method that performs all the real work"""
        
        global layer_list
        global selectedLayer
        global layer_combobox
        layer_combobox = self.dlg.layer_combobox
        layer_list = []
        layers = self.iface.legendInterface().layers()
        selectedLayerIndex = layer_combobox.currentIndex()
        selectedLayer = layers[selectedLayerIndex]

        
        #清空combobox
        layer_combobox.clear()
        for layer in layers:
            layer_list.append(layer.name())
        layer_combobox.addItems(layer_list)
        #按下search_button執行search_do
        self.dlg.search_button.clicked.connect(self.search_do)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
