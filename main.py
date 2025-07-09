import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QDate
import sqlite3
import datetime


from ui_motogp_viewer import Ui_MainWindow


class DatabaseManager:
    """
    Manages all interactions with the SQLite database (motogp_database.db).
    Adapts to the existing 'grand_prix_race_winners' table structure without 'id' or '"Grand Prix"' columns.
    """

    def __init__(self, db_name="motogp_database.db"):
        self.db_name = db_name
        self.conn = None
        self.connect()

    def connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Database Connection Error",
                                 f"Could not connect to database: {e}\n"
                                 "The application will now exit.")
            sys.exit(1)



    def insert_entry(self, season, circuit, class_name, rider, constructor, country):
        """Inserts a new race/winner entry into the 'grand_prix_race_winners' table."""
        try:
            # "Grand Prix" column is not in the database, so it's not inserted
            self.cursor.execute("""
                INSERT INTO grand_prix_race_winners (Season, Circuit, Class, Rider, Constructor, Country)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (season, circuit, class_name, rider, constructor, country))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            QMessageBox.warning(None, "Input Error",
                                "An entry with this Season, Circuit, Class, and Rider already exists. Please ensure uniqueness.")
            return False
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Database Error", f"Error adding entry: {e}")
            return False

    def select_all_entries(self, search_term="", category_filter="All"):
        """
        Selects all entries from the 'grand_prix_race_winners' table,
        with optional search by 'Circuit' and filter by 'Class'.
        """
        query = """
            SELECT Season, Circuit, Class, Rider, Constructor, Country
            FROM grand_prix_race_winners
        """
        params = []
        conditions = []

        if search_term:
            conditions.append('Circuit LIKE ?')
            params.append('%' + search_term + '%')

        if category_filter != "All":
            conditions.append('Class = ?')
            params.append(category_filter)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY Season DESC, Circuit ASC"

        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

    def update_entry(self, original_season, original_circuit, original_class_name, original_rider,
                     new_season, new_circuit, new_class_name, new_rider, new_constructor, new_country):
        """
        Updates an existing entry in the 'grand_prix_race_winners' table using a composite key.
        """
        try:
            self.cursor.execute("""
                UPDATE grand_prix_race_winners
                SET Season = ?, Circuit = ?, Class = ?, Rider = ?, Constructor = ?, Country = ?
                WHERE Season = ? AND Circuit = ? AND Class = ? AND Rider = ?
            """, (new_season, new_circuit, new_class_name, new_rider, new_constructor, new_country,
                  original_season, original_circuit, original_class_name, original_rider))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            QMessageBox.warning(None, "Input Error",
                                "An entry with the new Season, Circuit, Class, and Rider already exists. Please ensure uniqueness.")
            return False
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Database Error", f"Error updating entry: {e}")
            return False

    def delete_entry(self, season, circuit, class_name, rider):
        """Deletes an entry from the 'grand_prix_race_winners' table using a composite key."""
        try:
            self.cursor.execute("""
                DELETE FROM grand_prix_race_winners
                WHERE Season = ? AND Circuit = ? AND Class = ? AND Rider = ?
            """, (season, circuit, class_name, rider))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Database Error", f"Error deleting entry: {e}")
            return False

    def get_unique_classes(self):
        """Retrieves unique 'Class' values for filtering."""
        self.cursor.execute(
            "SELECT DISTINCT Class FROM grand_prix_race_winners WHERE Class IS NOT NULL AND Class != '' ORDER BY Class ASC")
        return [row[0] for row in self.cursor.fetchall()]

    def get_unique_countries(self):
        """Retrieves unique 'Country' values for filtering and input."""
        self.cursor.execute(
            "SELECT DISTINCT Country FROM grand_prix_race_winners WHERE Country IS NOT NULL AND Country != '' ORDER BY Country ASC")
        return [row[0] for row in self.cursor.fetchall()]

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

class MotoGPApp(QMainWindow, Ui_MainWindow):
    """
    Main application window for the Moto GP World Championship Winners Management System.
    Handles GUI layout, user interactions, and integrates with the DatabaseManager.
    Adapted to work with the 'grand_prix_race_winners' table without 'id' or '"Grand Prix"' columns.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db_manager = DatabaseManager()

        self.setStatusBar(self.statusbar)


        self._current_selected_key = None


        self.season_input.setValidator(QIntValidator(1949, 2022))


        self.add_entry_button.clicked.connect(self.add_entry)
        self.update_entry_button.clicked.connect(self.update_entry)
        self.delete_entry_button.clicked.connect(self.delete_entry)
        self.clear_form_button.clicked.connect(self.clear_form)
        self.search_input.textChanged.connect(self.search_data)
        self.class_filter_combo.currentIndexChanged.connect(self.filter_data_by_class)
        self.data_table.clicked.connect(self.load_entry_to_form)
        self.load_all_data()
        self.populate_filters()



    def load_all_data(self, search_term="", class_filter="All"):
        """Loads all data from the database into the main table."""
        entries = self.db_manager.select_all_entries(search_term, class_filter)
        self.data_table.setRowCount(0)  # Clear existing rows
        for row_num, entry in enumerate(entries):
            self.data_table.insertRow(row_num)
            for col_num, data in enumerate(entry):
                self.data_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        self.statusBar().showMessage(f"Loaded {len(entries)} entries.", 3000)

    def search_data(self):
        """Triggers data loading based on the search input (by Circuit)."""
        search_text = self.search_input.text()
        current_filter = self.class_filter_combo.currentText()
        self.load_all_data(search_text, current_filter)

    def filter_data_by_class(self):
        """Filters data based on the selected class."""
        selected_class = self.class_filter_combo.currentText()
        search_text = self.search_input.text()  # Keep search text when filtering
        self.load_all_data(search_text, selected_class)

    def populate_filters(self):
        """Populates the class and country filter QComboBoxes with unique values from the database."""
        classes = self.db_manager.get_unique_classes()
        self.class_filter_combo.blockSignals(True)
        self.class_filter_combo.clear()
        self.class_filter_combo.addItem("All")
        self.class_filter_combo.addItems(sorted(classes))
        self.class_filter_combo.blockSignals(False)

        countries = self.db_manager.get_unique_countries()
        self.country_input.blockSignals(True)
        self.country_input.clear()
        self.country_input.addItem("")
        self.country_input.addItems(sorted(countries))
        self.country_input.blockSignals(False)

    def load_entry_to_form(self):
        """Loads selected entry data from the table into the input form."""
        selected_row = self.data_table.currentRow()
        if selected_row >= 0:
            season = self.data_table.item(selected_row, 0).text()
            circuit = self.data_table.item(selected_row, 1).text()
            class_name = self.data_table.item(selected_row, 2).text()
            rider = self.data_table.item(selected_row, 3).text()
            constructor = self.data_table.item(selected_row, 4).text()
            country = self.data_table.item(selected_row, 5).text()

            self._current_selected_key = (season, circuit, class_name, rider)

            self.season_input.setText(season)
            self.circuit_input.setText(circuit)
            self.class_input.setCurrentText(class_name)
            self.rider_input.setText(rider)
            self.constructor_input.setText(constructor)
            self.country_input.setCurrentText(country)
            self.statusBar().showMessage(f"Loaded entry for: {rider} ({circuit})", 2000)

    def add_entry(self):
        """Adds a new entry to the database."""
        season_str = self.season_input.text().strip()
        circuit = self.circuit_input.text().strip()
        class_name = self.class_input.currentText()
        rider = self.rider_input.text().strip()
        constructor = self.constructor_input.text().strip()
        country = self.country_input.currentText()

        if not season_str or not circuit or not rider:
            QMessageBox.warning(self, "Input Error", "Season, Circuit, and Rider cannot be empty.")
            return

        try:
            season = int(season_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Season must be a valid number.")
            return
        if self.db_manager.insert_entry(season, circuit, class_name, rider, constructor, country):
            QMessageBox.information(self, "Success", "Entry added successfully!")
            self.clear_form()
            self.load_all_data()
            self.populate_filters()
            self.statusBar().showMessage(f"Entry for '{rider}' added.", 3000)

    def update_entry(self):
        """Updates an existing entry in the database."""
        if not self._current_selected_key:
            QMessageBox.warning(self, "Selection Error", "Please select an entry to update from the table.")
            return

        original_season, original_circuit, original_class_name, original_rider = self._current_selected_key

        new_season_str = self.season_input.text().strip()
        new_circuit = self.circuit_input.text().strip()
        new_class_name = self.class_input.currentText()
        new_rider = self.rider_input.text().strip()
        new_constructor = self.constructor_input.text().strip()
        new_country = self.country_input.currentText()

        if not new_season_str or not new_circuit or not new_rider:
            QMessageBox.warning(self, "Input Error", "Season, Circuit, and Rider cannot be empty for update.")
            return

        try:
            new_season = int(new_season_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid Season format.")
            return
        if self.db_manager.update_entry(original_season, original_circuit, original_class_name, original_rider,
                                        new_season, new_circuit, new_class_name, new_rider, new_constructor,
                                        new_country):
            QMessageBox.information(self, "Success", "Entry updated successfully!")
            self.clear_form()
            self.load_all_data()
            self.populate_filters()
            self.statusBar().showMessage(f"Entry for '{new_rider}' updated.", 3000)

    def delete_entry(self):
        """Deletes an entry from the database."""
        if not self._current_selected_key:
            QMessageBox.warning(self, "Selection Error", "Please select an entry to delete from the table.")
            return

        original_season, original_circuit, original_class_name, original_rider = self._current_selected_key

        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete entry for: {original_rider} ({original_circuit}, {original_season})?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.db_manager.delete_entry(original_season, original_circuit, original_class_name, original_rider):
                QMessageBox.information(self, "Success", "Entry deleted successfully!")
                self.clear_form()
                self.load_all_data()
                self.populate_filters()
                self.statusBar().showMessage(f"Entry for {original_rider} deleted.", 3000)

    def clear_form(self):
        """Clears all input fields in the data entry form."""
        self._current_selected_key = None
        self.season_input.clear()
        self.circuit_input.clear()
        self.class_input.setCurrentIndex(0)
        self.rider_input.clear()
        self.constructor_input.clear()
        self.country_input.setCurrentIndex(0)
        self.statusBar().showMessage("Form cleared.", 1000)

    def closeEvent(self, event):
        """Handles the application close event, ensuring database connection is closed."""
        self.db_manager.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotoGPApp()
    window.show()
    sys.exit(app.exec_())
