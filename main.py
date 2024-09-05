import copy
import os
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QTabWidget, QHBoxLayout, QLabel

from abstraction import take_values_from_csv
from combined_view import CombinedView
from comparison_view import ComparisonView
from data_process import PostProcess
from individual_view import IndividualView
from process_tool import ProcessTool
from save_utility import test_mkdir


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        # Logo placeholder
        self.logo_label = QLabel("Logo", self)  # Replace with actual logo if available
        left_layout.addWidget(self.logo_label)

        self.buttons_tab = QTabWidget(self)
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
    def create_tab(self, tab_name, individual_callback, comparison_callback, combined_callback,test_type=None,e0=None,e1=None,e2=None,e3=None):
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        tab_widget.setLayout(tab_layout)

        save_button=QPushButton(tab_name+" Save", self)
        save_button.clicked.connect(lambda:test_mkdir(self.main_directory,test_type,e0,e1,e2,e3))
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

    def flight_test(self,e0=None,e1=None,e2=None,e3=None):
        test_type = 2
        flight_e0 =None
        flight_e1=None
        flight_e2=None
        flight_e3=None
        if e0:
            flight_e0 = copy.deepcopy(PostProcess(e0,type=test_type))
        if e1:
            flight_e1 = copy.deepcopy(PostProcess(e1,type=test_type))
        if e2:
            flight_e2 = copy.deepcopy(PostProcess(e2,type=test_type))
        if e3:
            flight_e3 = copy.deepcopy(PostProcess(e3,type=test_type))

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
            combined_e0 = copy.deepcopy(PostProcess(e0, type=test_type, esc_id=0))
        if e1:
            combined_e1 = copy.deepcopy(PostProcess(e1, type=test_type, esc_id=1))
        if e2:
            combined_e2 = copy.deepcopy(PostProcess(e2, type=test_type, esc_id=2))
        if e3:
            combined_e3 = copy.deepcopy(PostProcess(e3, type=test_type, esc_id=3))

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
            step_e0 = copy.deepcopy(PostProcess(e0, type=test_type))
        if e1:
            step_e1 = copy.deepcopy(PostProcess(e1, type=test_type))
        if e2:
            step_e2 = copy.deepcopy(PostProcess(e2, type=test_type))
        if e3:
            step_e3 = copy.deepcopy(PostProcess(e3, type=test_type))

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
                        print("esc0 Loaded.")
                    elif actual_file == "esc1.csv" and "esc1.csv" not in loaded_files:
                        self.esc1_data = take_values_from_csv(Path(file_path))
                        loaded_files.add("esc1.csv")
                        print("esc1 Loaded.")
                    elif actual_file == "esc2.csv" and "esc2.csv" not in loaded_files:
                        self.esc2_data = take_values_from_csv(Path(file_path))
                        loaded_files.add("esc2.csv")
                        print("esc2 Loaded.")
                    elif actual_file == "esc3.csv" and "esc3.csv" not in loaded_files:
                        self.esc3_data = take_values_from_csv(Path(file_path))
                        loaded_files.add("esc3.csv")
                        print("esc3 Loaded.")
                else:
                    print(f"Unexpected file found: {actual_file}")
            except Exception as e:
                print(f"Error processing {actual_file}: {e}")

        # Check for any missing expected files
        for expected_file in expected_files:
            if expected_file not in loaded_files:
                print(f"{expected_file} is missing and was not loaded.")

    def load_data_button(self):
            try:
                self.process_files(self.files_path)
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
                print(f"An error occurred: {e}")
                self.tool_button.setEnabled(False)
                self.load_label.setText("Error occurred")
                self.path_display_widget.setStyleSheet("background-color: gray;")


    def open_folder_browser(self):
        self.files_path.clear()
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        dir_temp=str(folder_name)
        if folder_name:
            print(f"Selected folder: {folder_name}")
            self.main_directory=str(dir_temp)
            valid_folder = False

            for i in range(4):
                csv_name = os.path.join(folder_name, f"esc{i}.csv")
                if os.path.isfile(csv_name):
                    self.files_path.append(csv_name)
                    valid_folder = True
                else:
                    print(f"File not found: {csv_name}")

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
