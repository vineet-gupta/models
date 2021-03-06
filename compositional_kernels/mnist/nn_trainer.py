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

"""MNIST Trainer.
"""
import tensorflow as tf

from base import config
import base.nn_trainer as NN
import mnist_data_provider


def main(unused_argv):
  mnist_config = mnist_data_provider.GetMnistConfig()
  mnist_config.SetValueIfUnset(
      'skeleton_proto',
      'mnist/mnist.pb.txt')
  mnist_config.SetValueIfUnset('model_file_path', 'mnist/')
  mnist_config.SetValueIfUnset('number_of_epochs', 3)
  mnist_config.SetValueIfUnset('learning_rate', 0.01)
  mnist_config.SetValueIfUnset('optimizer', 'SGD')
  mnist_config.SetValueIfUnset('base_data_dir',
                               ('mnist/datasets/'))
  mnist_config.SetValueIfUnset('log_file', '')

  with tf.Graph().as_default(), tf.Session() as sess:
    train_provider = mnist_data_provider.MNIST_Input(mnist_config, 'train')
    test_provider = mnist_data_provider.MNIST_Input(mnist_config, 'test')
    batch_size = mnist_config.batch_size
    _, features, labels = train_provider.ProvideData(batch_size)
    _, test_features, test_labels = test_provider.ProvideData(batch_size)

    nn_model = NN.NeuralNetModel(
        mnist_config, features, labels, test_features, test_labels)

    nn_model.Init(sess)
    nn_model.Train(sess)


if __name__ == '__main__':
  tf.app.run()
