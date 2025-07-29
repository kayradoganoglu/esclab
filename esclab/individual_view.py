import tempfile

import pandas as pd
import plotly.express as px
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QDialog, QTabWidget

from abstraction import EscData
from PyQt6.QtWidgets import QCheckBox, QPushButton
from scipy.signal import savgol_filter



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

        # Ana layout
        layout = QVBoxLayout()

        # ✅ Wrapper widget ve layout (buton + tablar için)
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setSpacing(5)
        wrapper_layout.setContentsMargins(5, 5, 5, 5)
        wrapper.setLayout(wrapper_layout)

        # 🔹 Smoothing Toggle Button
        self.smoothing_enabled = False
        self.smooth_button = QPushButton("Toggle Smoothing Curve")
        self.smooth_button.setCheckable(True)
        self.smooth_button.setFixedWidth(250)
        self.smooth_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #888;
                font-weight: bold;
                font-size: 13px;
                padding: 6px;
                border-radius: 6px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:checked {
                background-color: #a0c4ff;
            }
        """)
        self.smooth_button.clicked.connect(self.toggle_smoothing)
        wrapper_layout.addWidget(self.smooth_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # 🔹 ESC Tabları
        self.tab_widget = QTabWidget()
        wrapper_layout.addWidget(self.tab_widget)

        # ✅ Wrapper'ı ana layout’a ekle
        layout.addWidget(wrapper)
        self.setLayout(layout)

        # 🔹 Sekmeleri oluştur
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
                'RPM': self.esc0.rpm,
                'Throttle Duty': self.esc0.t_duty,
                'Motor Duty': self.esc0.m_duty,
                'Phase Current': self.esc0.phase_current,
                'Power': self.esc0.pwr,
                'Status 1': self.esc0.stat_1,
                'Status 2': self.esc0.stat_2,
                'Serial Number': self.esc0.serial_number
            })
            if self.smoothing_enabled:
                for col in ['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power']:
                    if len(df[col]) >= 201:
                        df[col] = savgol_filter(df[col], window_length=201, polyorder=2)

            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-0'+'  '+'Serial Number'+ self.esc0.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_2(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc1.voltage))),
                'Voltage': self.esc1.voltage,
                'Current': self.esc1.current,
                'Temperature': self.esc1.temp,
                'eRPM': self.esc1.e_rpm,
                'RPM': self.esc1.rpm,
                'Throttle Duty': self.esc1.t_duty,
                'Motor Duty': self.esc1.m_duty,
                'Phase Current': self.esc1.phase_current,
                'Power': self.esc1.pwr,
                'Status 1': self.esc1.stat_1,
                'Status 2': self.esc1.stat_2,
                'Serial Number': self.esc1.serial_number
            })
            if self.smoothing_enabled:
                for col in ['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power']:
                    if len(df[col]) >= 201:
                        df[col] = savgol_filter(df[col], window_length=201, polyorder=2)

            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-1'+'  '+'Serial Number'+ self.esc1.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_3(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc2.voltage))),
                'Voltage': self.esc2.voltage,
                'Current': self.esc2.current,
                'Temperature': self.esc2.temp,
                'eRPM': self.esc2.e_rpm,
                'RPM': self.esc2.rpm,
                'Throttle Duty': self.esc2.t_duty,
                'Motor Duty': self.esc2.m_duty,
                'Phase Current': self.esc2.phase_current,
                'Power': self.esc2.pwr,
                'Status 1': self.esc2.stat_1,
                'Status 2': self.esc2.stat_2,
                'Serial Number': self.esc2.serial_number
            })
            if self.smoothing_enabled:
                for col in ['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power']:
                    if len(df[col]) >= 201:
                        df[col] = savgol_filter(df[col], window_length=201, polyorder=2)

            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-2'+'  '+'Serial Number'+ self.esc2.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_4(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc3.voltage))),
                'Voltage': self.esc3.voltage,
                'Current': self.esc3.current,
                'Temperature': self.esc3.temp,
                'eRPM': self.esc3.e_rpm,
                'RPM': self.esc3.rpm,
                'Throttle Duty': self.esc3.t_duty,
                'Motor Duty': self.esc3.m_duty,
                'Phase Current': self.esc3.phase_current,
                'Power': self.esc3.pwr,
                'Status 1': self.esc3.stat_1,
                'Status 2': self.esc3.stat_2,
                'Serial Number': self.esc3.serial_number
            })

            if self.smoothing_enabled:
                for col in ['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power']:
                    if len(df[col]) >= 201:
                        df[col] = savgol_filter(df[col], window_length=201, polyorder=2)

            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','RPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-3'+'  '+'Serial Number'+ self.esc3.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

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

    def refresh_tabs(self):
        self.tab_widget.clear()
        if self.esc0:
            self.create_tab("ESC 0", self.create_plot_1())
        if self.esc1:
            self.create_tab("ESC 1", self.create_plot_2())
        if self.esc2:
            self.create_tab("ESC 2", self.create_plot_3())
        if self.esc3:
            self.create_tab("ESC 3", self.create_plot_4())

    def toggle_smoothing(self):
        self.smoothing_enabled = not self.smoothing_enabled
        self.refresh_tabs()

