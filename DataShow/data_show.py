# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DataShow
                                 A QGIS plugin
 It's cool
                              -------------------
        begin                : 2017-07-12
        git sha              : $Format:%H$
        copyright            : (C) 2017 by CSMU
        email                : ol55432@yahoo.com.tw
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from data_show_dialog import DataShowDialog
import os.path
from qgis.core import QgsMapLayerRegistry, QgsField, QgsExpression, QgsFeature

class DataShow:
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
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DataShow_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&DataShow')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'DataShow')
        self.toolbar.setObjectName(u'DataShow')
        
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
        return QCoreApplication.translate('DataShow', message)


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
        self.dlg = DataShowDialog()

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

        icon_path = ':/plugins/DataShow/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&DataShow'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def refresh(self):
        global selectedLayer
        global dataArray
        global table
        
        selectedLayerIndex = self.dlg.comboBox.currentIndex()
        selectedLayer = layers[selectedLayerIndex]
        fields = selectedLayer.pendingFields()
        fieldname = [field.name() for field in fields]
        dataArray = []
        allDataArray = []
        dataLength = len([feat for feat in selectedLayer.getFeatures()])
        table = QTableWidget(dataLength, len(fieldname))
        table.setHorizontalHeaderLabels(fieldname)
        
        for feature in selectedLayer.getFeatures():
            data1 = str(feature.id())
            data2 = ','.join(unicode(feature[x]) for x in fieldname)
            splitData = data2.split(',')
            dataArray.append(splitData)
            data = data1 +','+ data2
            allData = data.split(',')
            allDataArray.append(allData)
            
        for i in range(dataLength):
            for j in range(len(fieldname)):
                newItem = QTableWidgetItem(dataArray[i][j])
                table.setItem(i, j, newItem)
        
        layout = self.dlg.formLayout
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
        table.cellChanged.connect(self.edit)
        layout.addRow(table)
        
    def add(self):
        if table.selectionModel().selectedColumns(True):
            #columnSelected = table.selectionModel().selectedColumns()
            #fields = [feat.id() for feat in selectedLayer.getFeatures()]
            fields = [field.name() for field in selectedLayer.pendingFields()]
            #for index in sorted(columnSelected):
            table.insertColumn(len(fields))
            selectedLayer.dataProvider().addAttributes([QgsField("new", QVariant.String)])
            selectedLayer.updateFields()
        elif table.selectionModel().selectedRows(True):
            #rowSelected = table.selectionModel().selectedRows()
            fields = [feat.id() for feat in selectedLayer.getFeatures()]
            #for index in sorted(rowSelected):
            table.insertRow(len(fields))
            updateFt = selectedLayer.dataProvider().addFeatures([QgsFeature()])
            #print fields
            return updateFt
            
    def delete(self):
        if table.selectionModel().selectedColumns(True):
            columnSelected = table.selectionModel().selectedColumns()
            for index in sorted(columnSelected):
                table.removeColumn(index.column())
                print index.column()
                selectedLayer.dataProvider().deleteAttributes([index.column()])
                selectedLayer.updateFields()

        elif table.selectionModel().selectedRows(True):
            rowSelected = table.selectionModel().selectedRows()
            fid = [feat.id() for feat in selectedLayer.getFeatures()]
            for index in sorted(rowSelected):
                table.removeRow(index.row())
                print fid[index.row()]
                updateFt = selectedLayer.dataProvider().deleteFeatures([fid[index.row()]])
                return updateFt
                
    def edit(self, row, column):
        editArray.append([row, column, table.item(row, column)])
        print editArray
        
    def run(self):
        """Run method that performs all the real work"""
        global layers
        global editArray
        editArray = []
        layers = self.iface.legendInterface().layers()
        layer_list = []
        
        for layer in layers:
            layer_list.append(layer.name())
        
        self.dlg.comboBox.addItems(layer_list)
        self.dlg.comboBox.currentIndexChanged.connect(self.refresh)
        self.refresh()
        
        self.dlg.pushButton.clicked.connect(self.add)
        self.dlg.pushButton_2.clicked.connect(self.delete)
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            columnCount = table.columnCount()
            rowCount = table.rowCount()
            updateArray2 = []
            
            for i in range(rowCount):
                updateArray1 = []
                for j in range(columnCount):
                    updateArray1.append(table.item(i, j))
                updateArray2.append(updateArray1)
            #print len(updateArray2[0])
            
            selectedLayer.startEditing()
            featureContent = [feat for feat in selectedLayer.getFeatures()]
            
            for i in editArray:
                featureContent[i[0]][i[1]] = (i[2]).text()
                selectedLayer.updateFeature(featureContent[i[0]])
                
            self.dlg.pushButton.clicked.disconnect(self.add)
            self.dlg.pushButton_2.clicked.disconnect(self.delete)
            """
            count = 0
            for feature in selectedLayer.getFeatures():
                for i in range(columnCount):
                    if updateArray2[count][i] is None:
                        feature[i] = ""
                        #print updateArray2[count][i].text()
                    else:
                        feature[i] = (updateArray2[count][i]).text()
                        #print updateArray2[count][i].text()
                    selectedLayer.updateFeature(feature)
                count = count + 1
            """
            pass
