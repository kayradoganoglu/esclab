import tempfile

import pandas as pd
import plotly.express as px
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QDialog, QTabWidget, QLabel, QDoubleSpinBox, QPushButton


from abstraction import EscData
from PyQt6.QtWidgets import QInputDialog
import plotly.graph_objs as go




class IndividualView(QDialog):
    def __init__(self,e0=None,e1=None,e2=None,e3=None):
        super().__init__()
        self.setWindowIcon(QIcon('data/logo.ico'))
        self.esc0=None
        self.esc1=None
        self.esc2=None
        self.esc3=None
        self.setWindowTitle("Individual View")
        self.setGeometry(150, 150, 800, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.tab_widget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
        from PyQt6.QtWidgets import QPushButton, QInputDialog
        self.rpm_button = QPushButton("Enable RPM Plot", self)
        self.rpm_button.clicked.connect(self.enable_rpm_plot)
        layout.addWidget(self.rpm_button)

        if e0:
            self.esc0 : EscData = e0
            self.create_tab("ESC 0", self.create_plot_1())
        if e1:
            self.esc1 : EscData = e1
            self.create_tab("ESC 1", self.create_plot_2())
        if e2:
            self.esc2 : EscData = e2
            self.create_tab("ESC 2", self.create_plot_3())
        if e3:
            self.esc3 : EscData = e3
            self.create_tab("ESC 3", self.create_plot_4())




    def create_plot_1(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc0.voltage))),
                'Voltage': self.esc0.voltage,
                'Current': self.esc0.current,
                'Temperature': self.esc0.temp,
                'eRPM': self.esc0.e_rpm,
                'RPM': [None] * len(self.esc0.e_rpm),
                'Throttle Duty': self.esc0.t_duty,
                'Motor Duty': self.esc0.m_duty,
                'Phase Current': self.esc0.phase_current,
                'Power': self.esc0.pwr,
                'Status 1': self.esc0.stat_1,
                'Status 2': self.esc0.stat_2,
                'Serial Number': self.esc0.serial_number
            })
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-0'+'  '+'Serial Number'+ self.esc0.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return go.Figure()

    def create_plot_2(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc1.voltage))),
                'Voltage': self.esc1.voltage,
                'Current': self.esc1.current,
                'Temperature': self.esc1.temp,
                'eRPM': self.esc1.e_rpm,
                'RPM': [None] * len(self.esc1.e_rpm),
                'Throttle Duty': self.esc1.t_duty,
                'Motor Duty': self.esc1.m_duty,
                'Phase Current': self.esc1.phase_current,
                'Power': self.esc1.pwr,
                'Status 1': self.esc1.stat_1,
                'Status 2': self.esc1.stat_2,
                'Serial Number': self.esc1.serial_number
            })
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-1'+'  '+'Serial Number'+ self.esc1.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return go.Figure()

    def create_plot_3(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc2.voltage))),
                'Voltage': self.esc2.voltage,
                'Current': self.esc2.current,
                'Temperature': self.esc2.temp,
                'eRPM': self.esc2.e_rpm,
                'RPM': [None] * len(self.esc2.e_rpm),
                'Throttle Duty': self.esc2.t_duty,
                'Motor Duty': self.esc2.m_duty,
                'Phase Current': self.esc2.phase_current,
                'Power': self.esc2.pwr,
                'Status 1': self.esc2.stat_1,
                'Status 2': self.esc2.stat_2,
                'Serial Number': self.esc2.serial_number
            })
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-2'+'  '+'Serial Number'+ self.esc2.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return go.Figure()

    def create_plot_4(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc3.voltage))),
                'Voltage': self.esc3.voltage,
                'Current': self.esc3.current,
                'Temperature': self.esc3.temp,
                'eRPM': self.esc3.e_rpm,
                'RPM': [None] * len(self.esc3.e_rpm),
                'Throttle Duty': self.esc3.t_duty,
                'Motor Duty': self.esc3.m_duty,
                'Phase Current': self.esc3.phase_current,
                'Power': self.esc3.pwr,
                'Status 1': self.esc3.stat_1,
                'Status 2': self.esc3.stat_2,
                'Serial Number': self.esc3.serial_number
            })
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-3'+'  '+'Serial Number'+ self.esc3.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return go.Figure()

    def create_tab(self, title, fig):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name

        browser = QWebEngineView()
        browser.setUrl(QUrl.fromLocalFile(tmp_file_path))

        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, title)

    def enable_rpm_plot(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("RPM Divisor")

        layout = QVBoxLayout(dialog)

        label = QLabel("Divide eRPM by:")
        layout.addWidget(label)

        # Açıklama metni
        note = QLabel("Info: RPM is typically calculated by dividing the eRPM value by 19.")
        note.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(note)

        spinbox = QDoubleSpinBox()
        spinbox.setRange(0.1, 100.0)
        spinbox.setValue(19.0)
        spinbox.setDecimals(2)
        layout.addWidget(spinbox)

        button = QPushButton("OK")
        layout.addWidget(button)

        def on_ok():
            x = spinbox.value()
            for esc_index, esc in enumerate([self.esc0, self.esc1, self.esc2, self.esc3]):
                if esc:
                    self.update_rpm_in_tab(esc_index, x)
            dialog.accept()

        button.clicked.connect(on_ok)
        dialog.exec()



    def _create_plot_widget(self, fig):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name
        browser = QWebEngineView()
        browser.setUrl(QUrl.fromLocalFile(tmp_file_path))
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(browser)
        widget.setLayout(layout)
        return widget
    
    def update_rpm_in_tab(self, esc_index, x_value):
        esc = [self.esc0, self.esc1, self.esc2, self.esc3][esc_index]
        if esc:
            rpm_values = [val / x_value for val in esc.e_rpm]
            df = pd.DataFrame({
                'Index': list(range(len(esc.voltage))),
                'Voltage': esc.voltage,
                'Current': esc.current,
                'Temperature': esc.temp,
                'eRPM': esc.e_rpm,
                'RPM': rpm_values,
                'Throttle Duty': esc.t_duty,
                'Motor Duty': esc.m_duty,
                'Phase Current': esc.phase_current,
                'Power': esc.pwr,
                'Status 1': esc.stat_1,
                'Status 2': esc.stat_2,
                'Serial Number': esc.serial_number
            })

            fig = px.line(df, x='Index', y=[
                'Voltage','Current','Temperature','eRPM','RPM',
                'Throttle Duty','Motor Duty','Phase Current','Power'
            ], title=f'ESC-{esc_index}  Serial Number {esc.serial_number}')

            new_widget = self._create_plot_widget(fig)
            self.tab_widget.removeTab(esc_index)
            self.tab_widget.insertTab(esc_index, new_widget, f'ESC {esc_index}')


