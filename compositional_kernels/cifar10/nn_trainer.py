# Copyright 2017 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

""" CIFAR10 Neural Net Trainer.
"""
import tensorflow as tf

from base import config
from base import nn_trainer as NN
import cifar10_data_provider


def main(unused_argv):
  cifar10_config = cifar10_data_provider.GetCifar10Config()
  cifar10_config.SetValueIfUnset('skeleton_proto', 'cifar10/cifar10.pb.txt')
  cifar10_config.SetValueIfUnset('model_file_path', '/tmp/data/cifar10/')
  cifar10_config.SetValueIfUnset('number_of_epochs', 10)
  cifar10_config.SetValueIfUnset('learning_rate', 0.1)
  cifar10_config.SetValueIfUnset('optimizer', 'SGD')
  cifar10_config.SetValueIfUnset('base_data_dir', 'cifar10/datasets/')
  cifar10_config.SetValueIfUnset('log_file', '')

  with tf.Graph().as_default(), tf.Session() as sess:
    train_provider = cifar10_data_provider.CIFAR10_Input(cifar10_config, 'train')
    test_provider = cifar10_data_provider.CIFAR10_Input(cifar10_config, 'test')
    batch_size = cifar10_config.batch_size
    _, features, labels = train_provider.ProvideData(batch_size)
    _, test_features, test_labels = test_provider.ProvideData(batch_size)

    nn_model = NN.NeuralNetModel(
        cifar10_config, features, labels, test_features, test_labels)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess, coord)
    nn_model.Init(sess)
    nn_model.Train(sess)
    coord.request_stop()
    coord.join(threads)

if __name__ == '__main__':
  tf.app.run()
