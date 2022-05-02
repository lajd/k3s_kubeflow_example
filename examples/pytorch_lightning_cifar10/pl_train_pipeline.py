#!/usr/bin/env python3
# Ref: https://pytorch-lightning.readthedocs.io/en/stable/notebooks/lightning_examples/cifar10-baseline.html

import kfp.dsl as kfp


def training_op(
        lr: float=0.05,
        momentum: float=0.9,
        wd: float=5e-4,
        max_lr: float=0.1,
        batch_size: int = 64,
        num_workers: int = 8,
        max_epochs: int = 30,
        step_name: str = 'training'
):
  return kfp.ContainerOp(
    name=step_name,
    image='lajd94/kubeflow_examples:pytorch_lightning_example',
    command=['/bin/bash', '-c'],
    arguments=[
      f'python train.py'
      f' --lr {lr}'
      f' --momentum {momentum}'
      f' --wd {wd}'
      f' --max_lr {max_lr}'
      f' --batch_size {batch_size}'
      f' --num_workers {num_workers}'
      f' --max_epochs {max_epochs}'
    ],
    # TODO: Handle directory output
    # file_outputs={'output': '/opt/model/lightning_logs/'},
  )


@kfp.pipeline(
  name='Pipeline Example',
  description='Demonstrate the Kubeflow pipelines SDK'
)

def kubeflow_training(
    lr: kfp.PipelineParam = kfp.PipelineParam(name='lr', value=0.05),
    momentum: kfp.PipelineParam = kfp.PipelineParam(name='momentum', value=0.9),
    wd: kfp.PipelineParam = kfp.PipelineParam(name='wd', value=5e-4),
    max_lr: kfp.PipelineParam = kfp.PipelineParam(name='max_lr', value=0.1),
    batch_size: kfp.PipelineParam = kfp.PipelineParam(name='batch_size', value=64),
    num_workers: kfp.PipelineParam = kfp.PipelineParam(name='num_workers', value=8),
    max_epochs: kfp.PipelineParam = kfp.PipelineParam(name='max_epochs', value=30),
  ):

  training = training_op(lr, momentum, wd, max_lr, batch_size, num_workers, max_epochs)


if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(kubeflow_training, __file__ + '.tar.gz')
