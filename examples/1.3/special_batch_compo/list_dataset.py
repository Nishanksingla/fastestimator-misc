import pdb
from os import pipe

from torch.utils.data import Dataset

import fastestimator as fe
from fastestimator.architecture.tensorflow import LeNet
from fastestimator.dataset import BatchDataset
from fastestimator.dataset.data import mnist
from fastestimator.op.numpyop.univariate import ExpandDims, Minmax
from fastestimator.op.tensorop import TensorOp
from fastestimator.op.tensorop.loss import CrossEntropy
from fastestimator.op.tensorop.model import ModelOp, UpdateOp


class NegativeImageSimulatedTube(Dataset):
    def __init__(self, ds):
        self.ds = ds

    def __getitem__(self, idx):
        # create your 5 simulated image here, for simplicity, I will just copy the same image 5 times
        image = self.ds[idx]["x"]
        label = self.ds[idx]["y"]
        return [{"x": image, "y": label} for _ in range(5)]

    def __len__(self):
        return len(self.ds)


def get_estimator():
    ds, _ = mnist.load_data()
    ds = NegativeImageSimulatedTube(ds)
    pipeline = fe.Pipeline(train_data=ds, ops=[ExpandDims(inputs="x", outputs="x"), Minmax(inputs="x", outputs="x")])
    model = fe.build(model_fn=LeNet, optimizer_fn="adam")
    network = fe.Network(ops=[
        ModelOp(model=model, inputs="x", outputs="y_pred"),
        CrossEntropy(inputs=("y_pred", "y"), outputs="ce"),
        UpdateOp(model=model, loss_name="ce")
    ])
    estimator = fe.Estimator(pipeline=pipeline, network=network, epochs=2)
    return estimator
