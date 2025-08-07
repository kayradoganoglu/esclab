
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QCheckBox,
    QPushButton, QHBoxLayout, QMessageBox
)

class ReportDialog(QDialog):
    def __init__(self, post_process=False, e0=None, e1=None, e2=None, e3=None):
        super().__init__()
        self.e0 = e0
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.post_process = post_process
        self.setWindowTitle("Generate Report - Selection")
        self.setMinimumWidth(400)

        self.selected_attributes = []
        self.selected_escs = []

        self.layout = QVBoxLayout()

        # Title
        title_label = QLabel("<b>Select Attributes to Include in Report</b>")
        self.layout.addWidget(title_label)

        # Attribute checkbox list
        self.attribute_checkboxes = []
        if not self.post_process:
            attribute_names = [      # Raw
                "Voltage", "Current", "Temperature", "eRPM", "RPM",
                "Throttle Duty", "Motor Duty", "Phase Current", "Power",
                "Status 1", "Status 2"
            ]
        else:
            attribute_names = [      # Post Process
                "Voltage", "Current", "Temperature", "RPM",
                "Throttle Duty", "Motor Duty", "Phase Current", "Power"
            ]


        for attr in attribute_names:
            checkbox = QCheckBox(attr)
            checkbox.setChecked(True)
            self.layout.addWidget(checkbox)
            self.attribute_checkboxes.append(checkbox)

        # ESC Seçimi
        esc_label = QLabel("<b>Select ESCs to Include</b>")
        self.layout.addWidget(esc_label)

        self.esc_checkboxes = []
        for i in range(4):
            esc_box = QCheckBox(f"ESC{i}")
            esc_box.setChecked(True)
            self.layout.addWidget(esc_box)
            self.esc_checkboxes.append(esc_box)

        # Buton
        self.generate_button = QPushButton("Generate PDF")
        self.generate_button.clicked.connect(self.on_generate_clicked)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

    def on_generate_clicked(self):
        self.selected_attributes = [
            cb.text() for cb in self.attribute_checkboxes if cb.isChecked()
        ]
        self.selected_escs = [
            i for i, cb in enumerate(self.esc_checkboxes) if cb.isChecked()
        ]

        if not self.selected_attributes:
            QMessageBox.warning(self, "Warning", "Please select at least one attribute.")
            return
        if not self.selected_escs:
            QMessageBox.warning(self, "Warning", "Please select at least one ESC.")
            return

        self.accept()  # Dialog closed successfully
