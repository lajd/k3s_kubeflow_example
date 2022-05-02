import os
import argparse
import json
from loguru import logger
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from pl_bolts.datamodules import CIFAR10DataModule
from pl_bolts.transforms.dataset_normalizations import cifar10_normalization
from pytorch_lightning import LightningModule, Trainer, seed_everything
from pytorch_lightning.callbacks import LearningRateMonitor
from pytorch_lightning.loggers import TensorBoardLogger
from torch.optim.lr_scheduler import OneCycleLR
from torch.optim.swa_utils import AveragedModel, update_bn
from torchmetrics.functional import accuracy

seed_everything(7)

PATH_DATASETS = os.environ.get("PATH_DATASETS", ".")
AVAIL_GPUS = min(1, torch.cuda.device_count())
DEFAULT_BATCH_SIZE = 256 if AVAIL_GPUS else 64
DEFAULT_NUM_WORKERS = int(os.cpu_count() / 2)


def create_model():
    model = torchvision.models.resnet18(pretrained=False, num_classes=10)
    model.conv1 = nn.Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
    model.maxpool = nn.Identity()
    return model


class LitResnet(LightningModule):
    def __init__(
            self,
            lr=0.05,
            momentum=0.9,
            wd=5e-4,
            max_lr=0.1,
            batch_size=DEFAULT_BATCH_SIZE,
    ):
        super().__init__()

        self.save_hyperparameters()
        self.model = create_model()

        logger.info(f"Hparams are:\n {repr(self.hparams)}")

    def forward(self, x):
        out = self.model(x)
        return F.log_softmax(out, dim=1)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        self.log("train_loss", loss)
        return loss

    def evaluate(self, batch, stage=None):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        preds = torch.argmax(logits, dim=1)
        acc = accuracy(preds, y)

        if stage:
            self.log(f"{stage}_loss", loss, prog_bar=True)
            self.log(f"{stage}_acc", acc, prog_bar=True)

    def validation_step(self, batch, batch_idx):
        self.evaluate(batch, "val")

    def test_step(self, batch, batch_idx):
        self.evaluate(batch, "test")

    def configure_optimizers(self):
        optimizer = torch.optim.SGD(
            self.parameters(),
            lr=self.hparams.lr,
            momentum=self.hparams.momentum,
            weight_decay=self.hparams.wd,
        )
        steps_per_epoch = 45000 // self.hparams.batch_size
        scheduler_dict = {
            "scheduler": OneCycleLR(
                optimizer,
                self.hparams.max_lr,
                epochs=self.trainer.max_epochs,
                steps_per_epoch=steps_per_epoch,
            ),
            "interval": "step",
        }
        return {"optimizer": optimizer, "lr_scheduler": scheduler_dict}

    @staticmethod
    def get_parsed_args():

        parser = argparse.ArgumentParser(description='ResNet18 Cifar10 Options')

        parser.add_argument('--lr', type=float, default=0.05, help='SGD Learning Rate')
        parser.add_argument('--momentum', type=float, default=0.9, help='SGD Momentum')
        parser.add_argument('--wd', type=float, default=5e-4, help='Weight Decay')
        parser.add_argument('--max_lr', type=float, default=0.1, help='Max Learning Rate')
        parser.add_argument('--batch_size', type=int, default=DEFAULT_BATCH_SIZE, help='Batch size')
        parser.add_argument('--num_workers', type=int, default=DEFAULT_NUM_WORKERS, help='Number of workers')
        parser.add_argument('--max_epochs', type=int, default=30, help='Number of epochs')

        args = parser.parse_args()
        return args


if __name__ == '__main__':
    parsed_args = LitResnet.get_parsed_args()

    logger.info(f"Parsed parameters are: {json.dumps(parsed_args.__dict__, indent=2)}")

    train_transforms = torchvision.transforms.Compose(
        [
            torchvision.transforms.RandomCrop(32, padding=4),
            torchvision.transforms.RandomHorizontalFlip(),
            torchvision.transforms.ToTensor(),
            cifar10_normalization(),
        ]
    )

    test_transforms = torchvision.transforms.Compose(
        [
            torchvision.transforms.ToTensor(),
            cifar10_normalization(),
        ]
    )

    cifar10_dm = CIFAR10DataModule(
        data_dir=PATH_DATASETS,
        batch_size=parsed_args.batch_size,
        num_workers=parsed_args.num_workers,
        train_transforms=train_transforms,
        test_transforms=test_transforms,
        val_transforms=test_transforms,
    )

    model = LitResnet(
        lr=parsed_args.lr,
        momentum=parsed_args.momentum,
        wd=parsed_args.wd,
        max_lr=parsed_args.max_lr,
        batch_size=parsed_args.batch_size,
    )
    model.datamodule = cifar10_dm

    trainer = Trainer(
        progress_bar_refresh_rate=10,
        max_epochs=parsed_args.max_epochs,
        gpus=AVAIL_GPUS,
        logger=TensorBoardLogger("lightning_logs/", name="resnet"),
        callbacks=[LearningRateMonitor(logging_interval="step")],
    )

    trainer.fit(model, cifar10_dm)
    trainer.test(model, datamodule=cifar10_dm)
