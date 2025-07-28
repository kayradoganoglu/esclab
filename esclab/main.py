import copy
import os
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QTabWidget, QHBoxLayout, QLabel
from abstraction import take_values_from_csv
from combined_view import CombinedView
from comparison_view import ComparisonView
from data_process import PostProcess
from individual_view import IndividualView
from process_tool import ProcessTool
from save_utility import test_mkdir
from console_widget import ConsoleWidget
from PyQt6.QtWidgets import QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(os.path.abspath(os.path.join(base_dir,'data','logo.ico'))))
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 900, 400)
        self.main_directory=None
        self.files_path = []

        self.esc0_data =None
        self.esc1_data =None
        self.esc2_data =None
        self.esc3_data =None

        self.post_process_esc0 =[]
        self.post_process_esc1 =[]
        self.post_process_esc2 =[]
        self.post_process_esc3 =[]

        self.folder_selected = False

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Left side layout
        left_layout = QVBoxLayout()
        left_layout.setSpacing(30)
        main_layout.addLayout(left_layout, stretch=3)


        self.logo_label = QLabel("Logo", self)
        logo_path= os.path.abspath(os.path.join(base_dir,"data", "logo.png"))
        pixmap=QPixmap(logo_path)
        print(logo_path)
        scaled_pixmap = pixmap.scaled(150,150, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        left_layout.addWidget(self.logo_label)

        self.buttons_tab = QTabWidget(self)
        self.buttons_tab.setTabsClosable(True)
        self.buttons_tab.tabCloseRequested.connect(self.close_tab)
        left_layout.addWidget(self.buttons_tab)

        self.raw_tab_created = False
        self.step_test_tab_created = False
        self.combined_step_test_tab_created = False
        self.flight_test_tab_created = False

        # Right side layout
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        main_layout.addLayout(right_layout, stretch=1)

        self.folder_button = QPushButton("Select Folder", self)
        self.folder_button.clicked.connect(self.open_folder_browser)
        right_layout.addWidget(self.folder_button)
        
        self.path_display_widget = QWidget()
        self.path_display_widget.setFixedHeight(30)
        right_layout.addWidget(self.path_display_widget)

        self.path_label = QLabel("No folder selected", self)
        self.path_display_widget_layout = QVBoxLayout()
        self.path_display_widget.setLayout(self.path_display_widget_layout)
        self.path_display_widget_layout.addWidget(self.path_label)
        self.path_display_widget.setStyleSheet("background-color: gray;")

        self.pole_value = 23

        # Pole Input UI
        self.pole_label = QLabel("<b> Enter Pole Pair Value :", self)
        right_layout.addWidget(self.pole_label)

        self.pole_input = QLineEdit(self)
        self.pole_input.setPlaceholderText("Enter Pole Pair Value (Default Value is 23):")
        self.pole_input.setText("23")  # Default Value Means that when this are is empty the application wont't crush.
        right_layout.addWidget(self.pole_input)


        self.load_button = QPushButton("Load Data", self)
        self.load_button.clicked.connect(self.load_data_button)
        self.load_button.setEnabled(True)
        right_layout.addWidget(self.load_button)

        self.load_display_widget = QWidget()
        self.load_display_widget.setFixedHeight(30)
        right_layout.addWidget(self.load_display_widget)

        self.load_label = QLabel("Files not Loaded!", self)
        self.load_display_widget_layout = QVBoxLayout()
        self.load_display_widget.setLayout(self.load_display_widget_layout)
        self.load_display_widget_layout.addWidget(self.load_label)
        self.load_display_widget.setStyleSheet("background-color: gray;")



        self.tool_button = QPushButton("Process Tool",self)
        self.tool_button.clicked.connect(self.open_process_tool_window)
        self.tool_button.setEnabled(False)
        right_layout.addWidget(self.tool_button)

        self.console= ConsoleWidget()
        right_layout.addWidget(self.console)

    def create_tab_raw(self, tab_name, individual_callback, comparison_callback, combined_callback):
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        tab_widget.setLayout(tab_layout)


        individual_view_button = QPushButton("Individual View", self)
        individual_view_button.clicked.connect(individual_callback)
        individual_view_button.setFixedHeight(60)
        tab_layout.addWidget(individual_view_button)

        comparison_view_button = QPushButton("Comparison View", self)
        comparison_view_button.clicked.connect(comparison_callback)
        comparison_view_button.setFixedHeight(60)
        tab_layout.addWidget(comparison_view_button)

        combined_view_button = QPushButton("Combined View", self)
        combined_view_button.clicked.connect(combined_callback)
        combined_view_button.setFixedHeight(60)
        tab_layout.addWidget(combined_view_button)

        self.buttons_tab.addTab(tab_widget, tab_name)
        self.console.log(f'>{tab_name} Data Tab Loaded')
    def create_tab(self, tab_name, individual_callback, comparison_callback, combined_callback,test_type=None,e0=None,e1=None,e2=None,e3=None):
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        tab_widget.setLayout(tab_layout)

        save_button=QPushButton(tab_name+" Save", self)
        save_button.clicked.connect(lambda:test_mkdir(self.main_directory,test_type,e0,e1,e2,e3,self.console))
        save_button.setFixedHeight(60)
        tab_layout.addWidget(save_button)

        individual_view_button = QPushButton("Individual View", self)
        individual_view_button.clicked.connect(individual_callback)
        individual_view_button.setFixedHeight(60)
        tab_layout.addWidget(individual_view_button)

        comparison_view_button = QPushButton("Comparison View", self)
        comparison_view_button.clicked.connect(comparison_callback)
        comparison_view_button.setFixedHeight(60)
        tab_layout.addWidget(comparison_view_button)

        combined_view_button = QPushButton("Combined View", self)
        combined_view_button.clicked.connect(combined_callback)
        combined_view_button.setFixedHeight(60)
        tab_layout.addWidget(combined_view_button)

        self.buttons_tab.addTab(tab_widget, tab_name)
        self.console.log(f'>{tab_name} Data Tab loaded')

    def close_tab(self,index):

        if self.buttons_tab.tabText(index) == "Raw":
            self.raw_tab_created=False
        if self.buttons_tab.tabText(index) == "Step Test":
            self.step_test_tab_created=False
        if self.buttons_tab.tabText(index) == "Combined Step Test":
            self.combined_step_test_tab_created=False
        if self.buttons_tab.tabText(index) == "Flight Test":
            self.flight_test_tab_created=False
        self.console.notify(f'>{self.buttons_tab.tabText(index)} Tab Closed : Data Erased')
        self.buttons_tab.removeTab(index)


    def flight_test(self,e0=None,e1=None,e2=None,e3=None):
        test_type = 2
        flight_e0=None
        flight_e1=None
        flight_e2=None
        flight_e3=None
        if e0:
            flight_e0 = copy.deepcopy(PostProcess(e0, type=test_type, pole_value=self.pole_value))
        if e1:
            flight_e1 = copy.deepcopy(PostProcess(e1, type=test_type, pole_value=self.pole_value))
        if e2:
            flight_e2 = copy.deepcopy(PostProcess(e2, type=test_type, pole_value=self.pole_value))
        if e3:
            flight_e3 = copy.deepcopy(PostProcess(e3, type=test_type, pole_value=self.pole_value))

        if not self.flight_test_tab_created:
            self.create_tab("Flight Test", self.open_individual_view_window,
                            lambda: self.open_comparison_view_window_flight_test(e0=flight_e0,e1=flight_e1,e2=flight_e2,e3=flight_e3),
                            lambda: self.open_combined_view_window_flight_test(e0=flight_e0,e1=flight_e1,e2=flight_e2,e3=flight_e3),
                            test_type,flight_e0,flight_e1,flight_e2,flight_e3)
            self.flight_test_tab_created = True

    def combined_step_test(self,e0=None,e1=None,e2=None,e3=None):
        test_type=1
        combined_e0 = None
        combined_e1 = None
        combined_e2 = None
        combined_e3 = None
        if e0:
            combined_e0 = copy.deepcopy(PostProcess(e0, type=test_type, esc_id=0, pole_value=self.pole_value))
        if e1:
            combined_e1 = copy.deepcopy(PostProcess(e1, type=test_type, esc_id=1, pole_value=self.pole_value))
        if e2:
            combined_e2 = copy.deepcopy(PostProcess(e2, type=test_type, esc_id=2, pole_value=self.pole_value))
        if e3:
            combined_e3 = copy.deepcopy(PostProcess(e3, type=test_type, esc_id=3, pole_value=self.pole_value))

        if not self.combined_step_test_tab_created:
            self.create_tab("Combined Step Test", self.open_individual_view_window,
                            lambda: self.open_comparison_view_window_combined_step_test(e0=combined_e0,e1=combined_e1,e2=combined_e2,e3=combined_e3),
                            lambda: self.open_combined_view_window_combined_step_test(e0=combined_e0,e1=combined_e1,e2=combined_e2,e3=combined_e3),
                            test_type,combined_e0,combined_e1,combined_e2,combined_e3)
            self.combined_step_test_tab_created = True
    def step_test(self,e0=None,e1=None,e2=None,e3=None):
        test_type = 0
        step_e0 = None
        step_e1 = None
        step_e2 = None
        step_e3 = None
        if e0:
            step_e0 = copy.deepcopy(PostProcess(e0, type=test_type, pole_value=self.pole_value))
        if e1:
            step_e1 = copy.deepcopy(PostProcess(e1, type=test_type, pole_value=self.pole_value))
        if e2:
            step_e2 = copy.deepcopy(PostProcess(e2, type=test_type, pole_value=self.pole_value))
        if e3:
            step_e3 = copy.deepcopy(PostProcess(e3, type=test_type, pole_value=self.pole_value))

        if not self.step_test_tab_created:
            self.create_tab("Step Test", self.open_individual_view_window,
                            lambda : self.open_comparison_view_window_step_test(e0=step_e0,e1=step_e1,e2=step_e2,e3=step_e3),
                            lambda : self.open_combined_view_window_step_test(e0=step_e0,e1=step_e1,e2=step_e2,e3=step_e3),
                            test_type, step_e0, step_e1, step_e2, step_e3)
            self.step_test_tab_created = True

    def process_files(self, file_paths):

        expected_files = ["esc0.csv", "esc1.csv", "esc2.csv", "esc3.csv"]
        loaded_files = set()

        # Iterate over the file paths
        for file_path in file_paths:
            try:
                # Extract the actual file name from the path
                actual_file = os.path.basename(file_path)

                # Check if the actual file is one of the expected files
                if actual_file in expected_files:
                    if actual_file == "esc0.csv" and "esc0.csv" not in loaded_files:
                        self.esc0_data = take_values_from_csv(Path(file_path))
                        loaded_files.add("esc0.csv")
                        self.console.log(">esc0 Loaded.")
                    elif actual_file == "esc1.csv" and "esc1.csv" not in loaded_files:
                        self.esc1_data = take_values_from_csv(Path(file_path))
                        loaded_files.add("esc1.csv")
                        self.console.log(">esc1 Loaded.")
                    elif actual_file == "esc2.csv" and "esc2.csv" not in loaded_files:
                        self.esc2_data = take_values_from_csv(Path(file_path))
                        loaded_files.add("esc2.csv")
                        self.console.log(">esc2 Loaded.")
                    elif actual_file == "esc3.csv" and "esc3.csv" not in loaded_files:
                        self.esc3_data = take_values_from_csv(Path(file_path))
                        loaded_files.add("esc3.csv")
                        self.console.log(">esc3 Loaded.")
                else:
                    self.console.alert(f"Unexpected file found: {actual_file}")
            except Exception as e:
                self.console.alert(f"Error processing {actual_file}: {e}")

        # Check for any missing expected files
        for expected_file in expected_files:
            if expected_file not in loaded_files:
                self.console.notify(f"{expected_file} is missing and was not loaded.")

    def load_data_button(self):
            try:
                self.process_files(self.files_path)

                try:
                    pole_value = float(self.pole_input.text().strip())
                except ValueError:
                    self.console.alert("Invalid Pole Value! Defaulting to 23.")
                    pole_value = 23.0

                self.pole_value = pole_value  # 🔴🔴 EKLENDİ
                self.console.log(f">Pole Pair Value: {self.pole_value} is added.")


                if self.esc0_data:
                    self.esc0_data.rpm = [erpm / pole_value for erpm in self.esc0_data.e_rpm]
                if self.esc1_data:
                    self.esc1_data.rpm = [erpm / pole_value for erpm in self.esc1_data.e_rpm]
                if self.esc2_data:
                    self.esc2_data.rpm = [erpm / pole_value for erpm in self.esc2_data.e_rpm]
                if self.esc3_data:
                    self.esc3_data.rpm = [erpm / pole_value for erpm in self.esc3_data.e_rpm]


                print("Pole Value:", pole_value)
                print("eRPM sample:", self.esc0_data.e_rpm[:5])
                print("RPM sample:", self.esc0_data.rpm[:5])

                print("LEN eRPM:", len(self.esc0_data.e_rpm))
                print("LEN RPM:", len(self.esc0_data.rpm))


                if self.esc0_data or self.esc1_data or self.esc2_data or self.esc3_data:
                    self.tool_button.setEnabled(True)
                if not self.raw_tab_created:
                    self.create_tab_raw("Raw", self.open_individual_view_window, self.open_comparison_view_window,
                                        self.open_combined_view_window)
                    self.raw_tab_created = True
                    self.tool_button.setEnabled(True)
                    self.load_label.setText("Files Loaded")
                    self.load_display_widget.setStyleSheet("background-color: green;")
            except Exception as e:
                self.console.log(f"An error occurred: {e}")
                self.tool_button.setEnabled(False)
                self.load_label.setText("Error occurred")
                self.path_display_widget.setStyleSheet("background-color: gray;")


    def open_folder_browser(self):
        self.files_path.clear()
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        dir_temp=str(folder_name)
        if folder_name:
            self.console.log(f"Selected folder: {folder_name}")
            self.main_directory=str(dir_temp)
            valid_folder = False

            for i in range(4):
                csv_name = os.path.join(folder_name, f"esc{i}.csv")
                if os.path.isfile(csv_name):
                    self.files_path.append(csv_name)
                    valid_folder = True
                else:
                    self.console.alert(f"File not found: {csv_name}")

            if self.files_path:
                self.load_button.setEnabled(True)
                self.esc0_data=None
                self.esc1_data=None
                self.esc2_data=None
                self.esc3_data=None
                # Enable button only if at least one file exists
            else:
                self.load_button.setEnabled(False)  # Disable button if no files are found

            self.path_label.setText(f"Selected Folder: {folder_name}")
            if valid_folder:
                self.path_display_widget.setStyleSheet("background-color: green;")
            else:
                self.path_display_widget.setStyleSheet("background-color: gray;")

            print(self.files_path)

    def open_individual_view_window(self):
        dialog = IndividualView(e0=self.esc0_data,e1=self.esc1_data,e2=self.esc2_data,e3=self.esc3_data)
        dialog.exec()
    def open_comparison_view_window(self):
        dialog = ComparisonView(e0=self.esc0_data,e1=self.esc1_data,e2=self.esc2_data,e3=self.esc3_data)
        dialog.exec()
    def open_combined_view_window(self):
        dialog = CombinedView(e0=self.esc0_data,e1=self.esc1_data,e2=self.esc2_data,e3=self.esc3_data)
        dialog.exec()
    def open_comparison_view_window_step_test(self,e0,e1,e2,e3):
        dialog = ComparisonView(e0=e0,e1=e1,e2=e2,e3=e3, post_process=True)
        dialog.exec()
    def open_combined_view_window_step_test(self,e0,e1,e2,e3):
        dialog = CombinedView(e0=e0,e1=e1,e2=e2,e3=e3, post_process=True)
        dialog.exec()
    def open_individual_view_window_combined_step_test(self):
        self.plot_window = IndividualView(e0=self.esc0_data,e1=self.esc1_data,e2=self.esc2_data,e3=self.esc3_data)
        self.plot_window.exec()
    def open_comparison_view_window_combined_step_test(self,e0,e1,e2,e3):
        dialog = ComparisonView(e0=e0,e1=e1,e2=e2,e3=e3, post_process=True)
        dialog.exec()
    def open_combined_view_window_combined_step_test(self,e0,e1,e2,e3):
        dialog = CombinedView(e0=e0,e1=e1,e2=e2,e3=e3, post_process=True)
        dialog.exec()
    def open_comparison_view_window_flight_test(self,e0,e1,e2,e3):
        dialog = ComparisonView(e0=e0,e1=e1,e2=e2,e3=e3, post_process=True)
        dialog.exec()
    def open_combined_view_window_flight_test(self,e0,e1,e2,e3):
        dialog = CombinedView(e0=e0,e1=e1,e2=e2,e3=e3, post_process=True)
        dialog.exec()
    def open_process_tool_window(self):
        dialog = ProcessTool(self)
        dialog.exec()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
