import copy
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import SpanSelector
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QGridLayout, QComboBox, QLabel, QWidget, QHBoxLayout, \
    QPushButton, QSpinBox, QCheckBox
from abstraction import EscData
from console_widget import ConsoleWidget

class ProcessTool(QDialog):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Process Tool")
        self.setGeometry(150, 150, 1408, 800)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        # Set up the QDialog layout
        main_layout = QVBoxLayout(self)
        layout = QGridLayout()
        main_layout.addLayout(layout)
        # Create a grid layout to hold the four plots
        grid_layout = QGridLayout()
        # Add the grid layout to the QDialog layout
        layout.addLayout(grid_layout,0,0)
        layout.setColumnStretch(1,2)
        self.esc0=None
        self.esc1=None
        self.esc2=None
        self.esc3=None
        if main_window.esc0_data:
            self.esc0 : EscData = main_window.esc0_data
        if main_window.esc1_data:
            self.esc1 : EscData = main_window.esc1_data
        if main_window.esc2_data:
            self.esc2 : EscData = main_window.esc2_data
        if main_window.esc3_data:
            self.esc3 : EscData = main_window.esc3_data
        self.cropped_esc0 = None
        self.cropped_esc1 = None
        self.cropped_esc2 = None
        self.cropped_esc3 = None
        self.crop_range = [(None,None),(None,None),(None,None),(None,None)]

        self.right_layout = QVBoxLayout()
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Step Test", "Combined Step Test", "Flight Test"])
        self.dropdown.setCurrentIndex(0)
        self.dropdown.currentIndexChanged.connect(self.dropdown_text_set)
        self.console=ConsoleWidget()
        # Content box that changes based on dropdown selection
        # Labels for x-axis range
        self.x_range_label_esc0 = QLabel("Esc 0 Range: Not selected")
        self.x_range_label_esc1 = QLabel("Esc 1 Range: Not selected")
        self.x_range_label_esc2 = QLabel("Esc 2 Range: Not selected")
        self.x_range_label_esc3 = QLabel("Esc 3 Range: Not selected")
        self.crop_button = QPushButton("Crop")
        self.crop_button.setEnabled(False)
        self.crop_button.clicked.connect(self.crop_data)
        self.post_process_run = QPushButton("Run Post-Process")
        self.post_process_run.clicked.connect(self.on_button_clicked)
        self.post_process_run.setEnabled(False)


        # Add dropdown, content label, and x-range label to right layout
        self.right_layout.addWidget(self.dropdown)
        self.right_layout.addWidget(self.crop_button)
        self.right_layout.addWidget(self.post_process_run)
        self.right_layout.addWidget(self.x_range_label_esc0)
        self.right_layout.addWidget(self.x_range_label_esc1)
        self.right_layout.addWidget(self.x_range_label_esc2)
        self.right_layout.addWidget(self.x_range_label_esc3)


        # Place Zero Utility
        self.max_range = []
        self.checkboxes = []
        self.selected_esc = None
        self.init_list=[]
        self.active_list=[]
        self.checked_num=None
        place_zero_button_layout = QHBoxLayout()
        self.place_zero_button = QPushButton("Place 0")
        self.place_zero_button.clicked.connect(self.place_zero)
        self.int_input = QSpinBox()
        self.input_esc = QComboBox()
        self.get_init_esc()
        print(self.active_list)
        self.index_get()
        self.input_esc.addItems(self.init_list)
        self.input_esc.setCurrentIndex(0)
        self.int_input.setMaximum(self.max_range[self.input_esc.currentIndex()])
        self.input_esc.currentIndexChanged.connect(self.update_max_index)
        self.int_input.setMinimum(0)
        place_zero_button_layout.addWidget(self.place_zero_button)
        place_zero_button_layout.addWidget(self.int_input)
        place_zero_button_layout.addWidget(self.input_esc)
        self.right_layout.addLayout(place_zero_button_layout)
        # Place Zero Utility

        self.create_checkbox()
        # Add the right layout to the main layout
        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)
        layout.addWidget(right_widget,0,1)

        self.right_layout.addStretch()
        self.right_layout.addWidget(self.console)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_layout.setSpacing(5)
        self.console.log("Process Tool Initialized.")

        self.fig, (self.ax0) = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.fig)
        # Add the canvas to the layout
        grid_layout.addWidget(self.canvas, 1, 0)
        grid_layout.addWidget(NavigationToolbar2QT(self.canvas, self), 0, 0)
        # Create a Matplotlib figure and axes
        if self.esc0:
            # Plot the data
            self.ax0.plot(self.esc0.timestamp, self.esc0.t_duty)
            self.ax0.set_ylim(-5, max(self.esc0.t_duty)+10)
            self.ax0.set_title('Esc 0')
            # Create the SpanSelector
            self.span0 = SpanSelector(
                self.ax0,
                self.onselect0,
                "horizontal",
                useblit=True,
                props=dict(alpha=0.5, facecolor="tab:blue"),
                interactive=True,
                drag_from_anywhere=True,
                ignore_event_outside=True,

            )
        else:
            # Set a title to indicate that no data is available
            self.ax0.set_title('Esc 0 (No Data)')
        # Create a Matplotlib figure and axes
        self.fig1, (self.ax1) = plt.subplots(figsize=(8, 6))
        self.canvas1 = FigureCanvas(self.fig1)
        # Add the canvas to the layout
        grid_layout.addWidget(self.canvas1, 1, 1)
        grid_layout.addWidget(NavigationToolbar2QT(self.canvas1, self), 0, 1)
        if self.esc1:
            # Plot the data
            self.ax1.plot(self.esc1.timestamp, self.esc1.t_duty)
            self.ax1.set_ylim(-5, max(self.esc1.t_duty)+10)
            self.ax1.set_title('Esc 1')
            # Create the SpanSelector
            self.span1 = SpanSelector(
                self.ax1,
                self.onselect1,
                "horizontal",
                useblit=True,
                props=dict(alpha=0.5, facecolor="tab:gray"),
                interactive=True,
                drag_from_anywhere=True,
                ignore_event_outside=True
            )
        else:
            # Set a title to indicate that no data is available
            self.ax1.set_title('Esc 1 (No Data)')
        # Create a Matplotlib figure and axes
        self.fig2, (self.ax2) = plt.subplots(figsize=(8, 6))
        self.canvas2 = FigureCanvas(self.fig2)
         # Add the canvas to the layout
        grid_layout.addWidget(self.canvas2,3,0)
        grid_layout.addWidget(NavigationToolbar2QT(self.canvas2, self), 2, 0)
        if self.esc2:
            # Plot the data
            self.ax2.plot(self.esc2.timestamp, self.esc2.t_duty)
            self.ax2.set_ylim(-5, max(self.esc2.t_duty)+10)
            self.ax2.set_title('Esc 2')
            # Create the SpanSelector
            self.span2 = SpanSelector(
                self.ax2,
                self.onselect2,
                "horizontal",
                useblit=True,
                props=dict(alpha=0.5, facecolor="tab:pink"),
                interactive=True,
                drag_from_anywhere=True,
                ignore_event_outside=True
            )
        else:
            # Set a title to indicate that no data is available
            self.ax2.set_title('Esc 2 (No Data)')

        # Create a Matplotlib figure and axes
        self.fig3, (self.ax3) = plt.subplots(figsize=(8, 6))
        self.canvas3 = FigureCanvas(self.fig3)
        # Add the canvas to the layout
        grid_layout.addWidget(self.canvas3, 3, 1)
        grid_layout.addWidget(NavigationToolbar2QT(self.canvas3, self), 2, 1)
        if self.esc3:
            # Plot the data
            self.ax3.plot(self.esc3.timestamp, self.esc3.t_duty)
            self.ax3.set_ylim(-5, max(self.esc3.t_duty)+10)
            self.ax3.set_title('Esc 3')
            # Create the SpanSelector
            self.span3 = SpanSelector(
                self.ax3,
                self.onselect3,
                "horizontal",
                useblit=True,
                props=dict(alpha=0.5, facecolor="tab:orange"),
                interactive=True,
                drag_from_anywhere=True,
                ignore_event_outside=True
            )
        else:
            # Set a title to indicate that no data is available
            self.ax3.set_title('Esc 3 (No Data)')

    def onselect0(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.esc0.timestamp, (xmin, xmax))
        indmax = min(len(self.esc0.timestamp) - 1, indmax)

        region_x = self.esc0.timestamp[indmin:indmax]
        region_y = self.esc0.t_duty[indmin:indmax]

        # Print the start and end indices to the console
        print(f"Plot0:Selected range: Start index = {indmin}, End index = {indmax}")
        self.x_range_label_esc0.setText(f'Esc 0 Range : {indmin},{indmax}')
        self.crop_range[0]=(int(indmin),int(indmax))
        self.check_crop()

    def onselect1(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.esc1.timestamp, (xmin, xmax))
        indmax = min(len(self.esc1.timestamp) - 1, indmax)

        region_x = self.esc1.timestamp[indmin:indmax]
        region_y = self.esc1.t_duty[indmin:indmax]

        # Print the start and end indices to the console
        print(f"Plot1:Selected range: Start index = {indmin}, End index = {indmax}")
        self.x_range_label_esc1.setText(f'Esc 1 Range : {indmin},{indmax}')
        self.crop_range[1] = (int(indmin), int(indmax))
        self.check_crop()

    def onselect2(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.esc2.timestamp, (xmin, xmax))
        indmax = min(len(self.esc2.timestamp) - 1, indmax)

        region_x = self.esc2.timestamp[indmin:indmax]
        region_y = self.esc2.t_duty[indmin:indmax]

        # Print the start and end indices to the console
        print(f"Plot2:Selected range: Start index = {indmin}, End index = {indmax}")
        self.x_range_label_esc2.setText(f'Esc 2 Range : {indmin},{indmax}')
        self.crop_range[2] = (int(indmin), int(indmax))
        self.check_crop()

    def onselect3(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.esc3.timestamp, (xmin, xmax))
        indmax = min(len(self.esc3.timestamp) - 1, indmax)

        region_x = self.esc3.timestamp[indmin:indmax]
        region_y = self.esc3.t_duty[indmin:indmax]

        # Print the start and end indices to the console
        print(f"Plot3:Selected range: Start index = {indmin}, End index = {indmax}")
        self.x_range_label_esc3.setText(f'Esc 3 Range : {indmin},{indmax}')
        self.crop_range[3] = (int(indmin), int(indmax))
        self.check_crop()
    def get_init_esc(self):
        if self.esc0:
            self.init_list.append("Esc 0")
            self.active_list.append(0)
        if self.esc1:
            self.init_list.append("Esc 1")
            self.active_list.append(1)
        if self.esc2:
            self.init_list.append("Esc 2")
            self.active_list.append(2)
        if self.esc3:
            self.init_list.append("Esc 3")
            self.active_list.append(3)

    def place_zero(self):
        value = self.int_input.value()
        esc = self.active_list[self.input_esc.currentIndex()]
        
        # Place zero in the selected ESC's data
        if esc == 0 and self.esc0:
            self.esc0.t_duty[value] = 0
            self.ax0.clear()
            self.ax0.plot(self.esc0.timestamp, self.esc0.t_duty)
            self.ax0.set_ylim(-5, max(self.esc0.t_duty)+10)
            self.ax0.set_title('Esc 0')
            self.canvas.draw()
            self.console.log(f'Place Zero ESC-0 at Index: {value}')
        elif esc == 1 and self.esc1:
            self.esc1.t_duty[value] = 0
            self.ax1.clear()
            self.ax1.plot(self.esc1.timestamp, self.esc1.t_duty)
            self.ax1.set_ylim(-5, max(self.esc1.t_duty)+10)
            self.ax1.set_title('Esc 1')
            self.canvas1.draw()
            self.console.log(f'Place Zero ESC-1 at Index: {value}')
        elif esc == 2 and self.esc2:
            self.esc2.t_duty[value] = 0
            self.ax2.clear()
            self.ax2.plot(self.esc2.timestamp, self.esc2.t_duty)
            self.ax2.set_ylim(-5, max(self.esc2.t_duty)+10)
            self.ax2.set_title('Esc 2')
            self.canvas2.draw()
            self.console.log(f'Place Zero ESC-2 at Index: {value}')
        elif esc == 3 and self.esc3:
            self.esc3.t_duty[value] = 0
            self.ax3.clear()
            self.ax3.plot(self.esc3.timestamp, self.esc3.t_duty)
            self.ax3.set_ylim(-5, max(self.esc3.t_duty)+10)
            self.ax3.set_title('Esc 3')
            self.canvas3.draw()
            self.console.log(f'Place Zero ESC-3 at Index: {value}')

    def check_crop(self):
        non_none_count = sum(1 for i in self.crop_range if i[0] is not None and i[1] is not None)

        if self.checked_num == 0:
            self.crop_button.setEnabled(False)
        elif non_none_count >= self.checked_num:
            self.crop_button.setEnabled(True)
        else:
            self.crop_button.setEnabled(False)

    def crop_data(self):
        range0=None
        range1=None
        range2=None
        range3=None
        if self.esc0:
            self.cropped_esc0 = copy.deepcopy(self.esc0)
            range0 = self.crop_range[0]
        if self.esc1:
            self.cropped_esc1 = copy.deepcopy(self.esc1)
            range1 = self.crop_range[1]
        if self.esc2:
            self.cropped_esc2 = copy.deepcopy(self.esc2)
            range2 = self.crop_range[2]
        if self.esc3:
            self.cropped_esc3 = copy.deepcopy(self.esc3)
            range3=self.crop_range[3]

        attribute_names=["voltage","current","temp","e_rpm","t_duty","m_duty","phase_current","pwr","stat_1","stat_2","timestamp"]
        for name in attribute_names:
            if self.cropped_esc0 and range0:
                attr0 = getattr(self.cropped_esc0, name)
                setattr(self.cropped_esc0, name, attr0[range0[0]:range0[1]])

            if self.cropped_esc1 and range1:
                attr1 = getattr(self.cropped_esc1, name)
                setattr(self.cropped_esc1, name, attr1[range1[0]:range1[1]])

            if self.cropped_esc2 and range2:
                attr2 = getattr(self.cropped_esc2, name)
                setattr(self.cropped_esc2, name, attr2[range2[0]:range2[1]])

            if self.cropped_esc3 and range3:
                attr3 = getattr(self.cropped_esc3, name)
                setattr(self.cropped_esc3, name, attr3[range3[0]:range3[1]])
        self.console.log(f'Data Cropped :{range0},{range1},{range2},{range3}')
        self.post_process_run.setEnabled(True)

    def on_button_clicked(self):

        for active in self.active_list:
            checkbox = self.checkboxes[active]
            if not checkbox.isChecked():
                # Dynamically set self.cropped_esc{active} to None
                setattr(self, f'cropped_esc{active}', None)

        if self.dropdown.currentIndex() == 0:
            self.main_window.step_test(e0=self.cropped_esc0, e1=self.cropped_esc1, e2=self.cropped_esc2, e3=self.cropped_esc3)
            self.console.log(f'>Step Test Initialized')
            if getattr(self.main_window,'step_test_tab_created'):
                self.console.log(f'>Step Test Created')
        elif self.dropdown.currentIndex() == 1:
            self.main_window.combined_step_test(e0=self.cropped_esc0, e1=self.cropped_esc1, e2=self.cropped_esc2, e3=self.cropped_esc3)
            self.console.log(f'>Combined Step Test Initialized')
            if getattr(self.main_window,'combined_step_test_tab_created'):
                self.console.log(f'>Combined Step Test Created')
        elif self.dropdown.currentIndex() == 2:
            self.main_window.flight_test(e0=self.cropped_esc0, e1=self.cropped_esc1, e2=self.cropped_esc2, e3=self.cropped_esc3)
            self.console.log(f'>Flight Test Initialized')
            if getattr(self.main_window,'flight_test_tab_created'):
                self.console.log(f'>Flight Test Created')

    def dropdown_text_set(self):
        if self.dropdown.currentIndex() == 0:
            self.post_process_run.setText("Run Step Test")
        elif self.dropdown.currentIndex() == 1:
            self.post_process_run.setText("Run Combined Step Test")
        elif self.dropdown.currentIndex() == 2:
            self.post_process_run.setText("Run Flight Test")

    def update_max_index(self):
        self.int_input.setMaximum(self.max_range[self.input_esc.currentIndex()])

    def create_checkbox(self):

        for i in range(4):
            checkbox = QCheckBox(f"Esc {i}")
            checkbox.setEnabled(False)  # Initially disable all checkboxes
            checkbox.setChecked(False)  # Set them all to checked by default
            checkbox.checkStateChanged.connect(self.check_num_update)
            checkbox.checkStateChanged.connect(self.check_crop)
            self.right_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        # Enable the checkboxes that correspond to indices in active_list
        for active in self.active_list:
            self.checkboxes[active].setChecked(True)
            self.checkboxes[active].setEnabled(True)
        self.check_num_update()

    def index_get(self):
        temp = []
        for active in self.active_list:
            temp = getattr(self,f'esc{active}',None)
            if temp is not None:
                self.max_range.append(len(temp.timestamp))
            else:
                self.console.alert("!!Unable to set maximum index")
        print(self.max_range)

    def check_num_update(self):
        num=0
        for active in self.active_list:
            if self.checkboxes[active].isChecked():
                num+=1
        self.checked_num = num
        print(self.checked_num)
