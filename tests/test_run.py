from mousetumornet import predict
import numpy as np

from mousetumornet.configuration import MODELS

def test_predict():
    """Runs the model prediction on a pseudo-image of random numbers."""
    image = np.random.random((256, 256, 256)).astype(np.float32)

    for model in MODELS.keys():
        pred = predict(image, model=model)
        assert pred.shape == image.shape, "Pred shape is erroneous."


# from mousetumornet.napari_nnunet import NNUNetWidget

# def test_nnunet_widget(make_napari_viewer):
#     viewer = make_napari_viewer()

#     # test_labels = np.arange(0, 9).reshape((3, 3))
#     # viewer.add_labels(test_labels)

#     widget = NNUNetWidget(viewer)
#     # assert len(my_widget.table._table) == len(np.unique(test_labels)) - 1

#     assert 0 == 0
