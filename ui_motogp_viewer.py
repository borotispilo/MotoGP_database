
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.central_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.central_widget.setObjectName("central_widget")
        self.data_viewer_tab = QtWidgets.QWidget()
        self.data_viewer_tab.setObjectName("data_viewer_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.data_viewer_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.form_layout = QtWidgets.QHBoxLayout()
        self.form_layout.setObjectName("form_layout")
        self.input_fields_layout = QtWidgets.QVBoxLayout()
        self.input_fields_layout.setObjectName("input_fields_layout")

        # Season
        self.season_label = QtWidgets.QLabel(self.data_viewer_tab)
        self.season_label.setObjectName("season_label")
        self.input_fields_layout.addWidget(self.season_label)
        self.season_input = QtWidgets.QLineEdit(self.data_viewer_tab)
        self.season_input.setPlaceholderText("e.g., 2022")
        self.season_input.setObjectName("season_input")
        self.input_fields_layout.addWidget(self.season_input)

        # Circuit
        self.circuit_label = QtWidgets.QLabel(self.data_viewer_tab)
        self.circuit_label.setObjectName("circuit_label")
        self.input_fields_layout.addWidget(self.circuit_label)
        self.circuit_input = QtWidgets.QLineEdit(self.data_viewer_tab)
        self.circuit_input.setPlaceholderText("e.g., Algarve International Circuit")
        self.circuit_input.setObjectName("circuit_input")
        self.input_fields_layout.addWidget(self.circuit_input)

        # Class
        self.class_label = QtWidgets.QLabel(self.data_viewer_tab)
        self.class_label.setObjectName("class_label")
        self.input_fields_layout.addWidget(self.class_label)
        self.class_input = QtWidgets.QComboBox(self.data_viewer_tab)
        self.class_input.setObjectName("class_input")
        self.class_input.addItems(["MotoGP", "Moto2", "Moto3", "500cc", "250cc", "125cc", "350cc", "80cc", "50cc"])
        self.input_fields_layout.addWidget(self.class_input)

        # Rider
        self.rider_label = QtWidgets.QLabel(self.data_viewer_tab)
        self.rider_label.setObjectName("rider_label")
        self.input_fields_layout.addWidget(self.rider_label)
        self.rider_input = QtWidgets.QLineEdit(self.data_viewer_tab)
        self.rider_input.setPlaceholderText("e.g., Marc Márquez")
        self.rider_input.setObjectName("rider_input")
        self.input_fields_layout.addWidget(self.rider_input)

        # Constructor
        self.constructor_label = QtWidgets.QLabel(self.data_viewer_tab)
        self.constructor_label.setObjectName("constructor_label")
        self.input_fields_layout.addWidget(self.constructor_label)
        self.constructor_input = QtWidgets.QLineEdit(self.data_viewer_tab)
        self.constructor_input.setPlaceholderText("e.g., Honda")
        self.constructor_input.setObjectName("constructor_input")
        self.input_fields_layout.addWidget(self.constructor_input)

        # Country
        self.country_label = QtWidgets.QLabel(self.data_viewer_tab)
        self.country_label.setObjectName("country_label")
        self.input_fields_layout.addWidget(self.country_label)
        self.country_input = QtWidgets.QComboBox(self.data_viewer_tab)
        self.country_input.setObjectName("country_input")
        self.input_fields_layout.addWidget(self.country_input)

        self.form_layout.addLayout(self.input_fields_layout)

        self.button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.setObjectName("button_layout")

        self.add_entry_button = QtWidgets.QPushButton(self.data_viewer_tab)
        self.add_entry_button.setObjectName("add_entry_button")
        self.button_layout.addWidget(self.add_entry_button)

        self.update_entry_button = QtWidgets.QPushButton(self.data_viewer_tab)
        self.update_entry_button.setObjectName("update_entry_button")
        self.button_layout.addWidget(self.update_entry_button)

        self.delete_entry_button = QtWidgets.QPushButton(self.data_viewer_tab)
        self.delete_entry_button.setObjectName("delete_entry_button")
        self.button_layout.addWidget(self.delete_entry_button)

        self.clear_form_button = QtWidgets.QPushButton(self.data_viewer_tab)
        self.clear_form_button.setObjectName("clear_form_button")
        self.button_layout.addWidget(self.clear_form_button)
        self.form_layout.addLayout(self.button_layout)
        self.form_layout.addStretch()
        self.verticalLayout_2.addLayout(self.form_layout)

        self.filter_search_layout = QtWidgets.QHBoxLayout()
        self.filter_search_layout.setObjectName("filter_search_layout")

        # Search by Circuit
        self.search_label = QtWidgets.QLabel(self.data_viewer_tab)
        self.search_label.setObjectName("search_label")
        self.filter_search_layout.addWidget(self.search_label)
        self.search_input = QtWidgets.QLineEdit(self.data_viewer_tab)
        self.search_input.setPlaceholderText("Search by Circuit...")
        self.search_input.setObjectName("search_input")
        self.filter_search_layout.addWidget(self.search_input)

        # Filter by Class
        self.class_filter_label = QtWidgets.QLabel(self.data_viewer_tab)
        self.class_filter_label.setObjectName("class_filter_label")
        self.filter_search_layout.addWidget(self.class_filter_label)
        self.class_filter_combo = QtWidgets.QComboBox(self.data_viewer_tab)
        self.class_filter_combo.setObjectName("class_filter_combo")
        self.class_filter_combo.addItem("All")
        self.filter_search_layout.addWidget(self.class_filter_combo)
        self.filter_search_layout.addStretch()
        self.verticalLayout_2.addLayout(self.filter_search_layout)

        # Table Display
        self.data_table = QtWidgets.QTableWidget(self.data_viewer_tab)
        self.data_table.setObjectName("data_table")
        self.data_table.setColumnCount(6) # Season, Circuit, Class, Rider, Constructor, Country
        self.data_table.setHorizontalHeaderLabels(["Season", "Circuit", "Class", "Rider", "Constructor", "Country"])
        self.data_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.data_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.verticalLayout_2.addWidget(self.data_table)

        self.central_widget.addTab(self.data_viewer_tab, "Moto GP Data Viewer")
        self.verticalLayout.addWidget(self.central_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.central_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Moto GP Winners Data Viewer"))
        self.season_label.setText(_translate("MainWindow", "Season:"))
        self.circuit_label.setText(_translate("MainWindow", "Circuit:"))
        self.class_label.setText(_translate("MainWindow", "Class:"))
        self.rider_label.setText(_translate("MainWindow", "Rider:"))
        self.constructor_label.setText(_translate("MainWindow", "Constructor:"))
        self.country_label.setText(_translate("MainWindow", "Country:"))
        self.add_entry_button.setText(_translate("MainWindow", "Add Entry"))
        self.update_entry_button.setText(_translate("MainWindow", "Update Entry"))
        self.delete_entry_button.setText(_translate("MainWindow", "Delete Entry"))
        self.clear_form_button.setText(_translate("MainWindow", "Clear Form"))
        self.search_label.setText(_translate("MainWindow", "Search:"))
        self.class_filter_label.setText(_translate("MainWindow", "Filter by Class:"))
        self.central_widget.setTabText(self.central_widget.indexOf(self.data_viewer_tab), _translate("MainWindow", "Moto GP Data Viewer"))

