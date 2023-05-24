import os
import sys

import napari.layers
from napari.qt.threading import thread_worker
from napari.utils.notifications import show_info
from napari_tools_menu import register_dock_widget
from PyQt5.QtCore import Qt
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from nnunet_predict import predict, postprocess


@register_dock_widget(menu="Detection > nnUNet")
class NNUNetWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        self.viewer = napari_viewer

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self)
        self.setLayout(layout)

        qw00 = QWidget(self)
        self.layout().addWidget(qw00)
        sub00 = QHBoxLayout()
        qw00.setLayout(sub00)
        sub00.addWidget(QLabel("Image", self))
        self.cb_image = QComboBox()
        sub00.addWidget(self.cb_image)

        btn = QPushButton("Detect tumors", self)
        btn.clicked.connect(self._trigger_long_process)
        self.layout().addWidget(btn)

        self.pbar = QProgressBar(self, minimum=0, maximum=0)
        self.pbar.setVisible(False)
        self.layout().addWidget(self.pbar)

        self.viewer.layers.events.inserted.connect(self._add_rename_event)
        self.viewer.layers.events.inserted.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._on_layer_change)
        self._on_layer_change(None)

    def _add_rename_event(self, e):
        source_layer = e.value
        source_layer.events.name.connect(self._proxy_on_layer_change)

    def _proxy_on_layer_change(self, e):
        self._on_layer_change(None)

    def long_process(self):
        image = self.cb_image.currentData()

        image_pred = predict(image)
        image_pred = postprocess(image_pred)

        image_pred = image_pred.astype('uint16')

        return image_pred

    @thread_worker
    def _long_process(self):
        self.segmentation = self.long_process()

    def _start_long_process(self):
        if self.cb_image.currentData() is None:
            return

        worker = self._long_process()
        worker.returned.connect(self._load_in_viewer)

        self.pbar.setVisible(True)
        worker.start()

        show_info("Tumor detection started...")

    def _trigger_long_process(self):
        self._start_long_process()

    def _load_in_viewer(self):
        """Callback from thread returning."""

        self.pbar.setVisible(False)

        if self.segmentation is not None:
            prob_layer = self.viewer.add_labels(self.segmentation, name="Tumors (nnUNet)")
            prob_layer.opacity = 0.2
            prob_layer.blending = "additive"

        show_info("Tumor detection finished!")

    def _on_layer_change(self, e):
        self.cb_image.clear()
        for x in self.viewer.layers:
            if isinstance(x, napari.layers.Image):
                self.cb_image.addItem(x.name, x.data)
