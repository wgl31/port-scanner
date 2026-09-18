# gui.py
# desktop GUI - PySide6 front end for the scanner

import sys
import threading

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QProgressBar, QPushButton, QSpinBox, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget,
)

from fingerprint import grab_banner, identify_service
from reporter import save_json
from resolver import resolve_target
from scanner import scan_target


class ScanWorker(QThread):
    port_found = Signal(dict)
    progress = Signal(int, int)
    finished = Signal(list)
    resolution_failed = Signal(str)

    def __init__(self, target, ports):
        super().__init__()
        self.target = target
        self.ports = ports
        self.cancel_event = threading.Event()

    def stop(self):
        self.cancel_event.set()

    def run(self):
        ips = resolve_target(self.target)
        if not ips:
            self.resolution_failed.emit(self.target)
            return

        results = []
        total = len(ips) * len(self.ports)
        scanned = 0

        for ip in ips:
            if self.cancel_event.is_set():
                break

            def on_progress(port, is_open, ip=ip):
                nonlocal scanned
                scanned += 1
                self.progress.emit(scanned, total)
                if is_open:
                    banner = grab_banner(ip, port)
                    service = identify_service(banner, port)
                    row = {'ip': ip, 'port': port, 'service': service}
                    results.append(row)
                    self.port_found.emit(row)

            scan_target(ip, self.ports, on_progress=on_progress, cancel_event=self.cancel_event)

        self.finished.emit(results)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Port Scanner")
        self.resize(600, 500)

        self.worker = None
        self.results = []

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Target IP, hostname or CIDR")

        self.start_port = QSpinBox()
        self.start_port.setRange(1, 65535)
        self.start_port.setValue(1)

        self.end_port = QSpinBox()
        self.end_port.setRange(1, 65535)
        self.end_port.setValue(1024)

        self.scan_button = QPushButton("Scan")
        self.scan_button.clicked.connect(self.start_scan)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_scan)
        self.stop_button.setEnabled(False)

        self.save_button = QPushButton("Save JSON")
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setEnabled(False)

        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("Target:"))
        top_row.addWidget(self.target_input)
        top_row.addWidget(QLabel("Ports:"))
        top_row.addWidget(self.start_port)
        top_row.addWidget(QLabel("-"))
        top_row.addWidget(self.end_port)
        top_row.addWidget(self.scan_button)
        top_row.addWidget(self.stop_button)

        self.progress_bar = QProgressBar()
        self.status_label = QLabel("Ready")

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["IP", "Port", "Service"])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout()
        layout.addLayout(top_row)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.table)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_scan(self):
        target = self.target_input.text().strip()
        if not target:
            QMessageBox.warning(self, "Missing target", "Enter a target IP, hostname or CIDR.")
            return

        start, end = self.start_port.value(), self.end_port.value()
        if start > end:
            QMessageBox.warning(self, "Invalid range", "Start port must be <= end port.")
            return
        ports = range(start, end + 1)

        self.results = []
        self.table.setRowCount(0)
        self.progress_bar.setValue(0)
        self.status_label.setText("Scanning...")
        self.scan_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.save_button.setEnabled(False)

        self.worker = ScanWorker(target, ports)
        self.worker.port_found.connect(self.add_result)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.scan_finished)
        self.worker.resolution_failed.connect(self.resolution_failed)
        self.worker.start()

    def stop_scan(self):
        if self.worker:
            self.worker.stop()
            self.status_label.setText("Stopping...")
            self.stop_button.setEnabled(False)

    def add_result(self, row):
        self.results.append(row)
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(row['ip']))
        self.table.setItem(r, 1, QTableWidgetItem(str(row['port'])))
        self.table.setItem(r, 2, QTableWidgetItem(row['service']))

    def update_progress(self, scanned, total):
        if total:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(scanned)

    def scan_finished(self, results):
        self.status_label.setText(f"Done - {len(results)} open port(s) found")
        self.scan_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.save_button.setEnabled(bool(results))

    def resolution_failed(self, target):
        self.status_label.setText(f"Could not resolve {target}")
        self.scan_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.save_button.setEnabled(False)

    def save_results(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save results", "results.json", "JSON files (*.json)")
        if filename:
            save_json(self.results, filename)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
