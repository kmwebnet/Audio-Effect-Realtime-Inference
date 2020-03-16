import os
import sys
from argparse import ArgumentParser
import time
import yaml
import numpy as np
from numpy.lib.stride_tricks import as_strided

import sounddevice as sd
from multiprocessing import Pool, Queue, Manager, TimeoutError

d_len = 0
q_out =None
in_buffer = np.zeros(0, np.float32)

nnp = None
p = None
xx = None
yy = None

def sliding_window(x, window, slide):
    n_slide = (len(x) - window) // slide
    remain = (len(x) - window) % slide
    clopped = x[:-remain]
    return as_strided(clopped, shape=(n_slide + 1, window), strides=(slide * 4, 4))

def init_worker():

    import nnabla as nn
    import nnabla.functions as F
    import nnabla.parametric_functions as PF
    #import nnabla.solvers as S
    from nnabla.utils.nnp_graph import NnpLoader


    nnp = NnpLoader("MyChain.nnp")
    net = nnp.get_network("MyChain", batch_size)

    global xx
    global yy

    xx = net.inputs['xx']
    yy = net.outputs['yy']


def processing(indata, q ):

    d_len = len(indata)

    padded = np.concatenate((
        np.zeros(prepad, np.float32),
        indata))

    x = sliding_window(padded, input_timesteps, output_timesteps)
    x = x[:, :, np.newaxis]
    xx.d = x

    yy.forward()

    time.sleep(0.4)

    q.put(yy.d[:, -output_timesteps:, :].reshape(-1)[:d_len])


def callback(in_data, out_data, frames, time, status):

    global q_out
    print("\r\033[1Aq_size", q_out.qsize())

    out_data[: ,0] = q_out.get()

    global in_buffer
    global nnp

    in_buffer = np.concatenate([in_buffer, in_data[: ,0]])

    if in_buffer.shape[0] == block_size:

        try:
            res= p.apply_async(processing, args=(in_buffer, q_out ,))  # Create new process
            res.get(timeout=0)
        except TimeoutError as err:
            pass


        in_buffer = np.zeros(0, np.float32)  # Empty the input buffer


def main():

    args = parse_args()

    with open(args.config_file) as fp:
        config = yaml.safe_load(fp)

    global input_timesteps
    global output_timesteps
    global batch_size
    global block_size
    global prepad
    global nnp
    global q_out
    global p


    input_timesteps = config["input_timesteps"]
    output_timesteps = config["output_timesteps"]
    batch_size = config["batch_size"]

    block_size = output_timesteps * batch_size
    prepad = input_timesteps - output_timesteps


    CHUNK= block_size
    RATE=48000

    """
    from nnabla.ext_utils import get_extension_context
    cuda_device_id = 0
    ctx = get_extension_context('cudnn', device_id=cuda_device_id)
    print("Context: {}".format(ctx))
    nn.set_default_context(ctx)  # Set CUDA as a default context.
    """


    p = Pool(processes=4 , initializer=init_worker)
    m = Manager()
    q_out = m.Queue(maxsize=0)

    time.sleep(1)


    for i in range(4):
        prefill = np.zeros(block_size, np.float32)
        p.apply(processing, args=(prefill, q_out ,))


    print("prepare done. wait 1sec")
    time.sleep(1)


    try:
        with sd.Stream(device=1,
                samplerate=RATE, blocksize=CHUNK,
                dtype=np.float32,
                channels=1,
                callback=callback,
                prime_output_buffers_using_stream_callback=True):
            print('#' * 80)
            print('press Return to quit')
            print('#' * 80)
            print(" ")
            input()
    except KeyboardInterrupt:
        parser.exit('')
        p.close()
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))




def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--config_file", "-c", default="./config.yml",
        help="configuration file (*.yml)")
    parser.add_argument(
        "--input_file", "-i",
        help="input wave file (48kHz/mono, *.wav)")
    parser.add_argument(
        "--output_file", "-o", default="./predicted-by-nnp.wav",
        help="output wave file (48kHz/mono, *.wav)")
    parser.add_argument(
        "--model_file", "-m",
        help="input model file (*.h5)")
    return parser.parse_args()

if __name__ == '__main__':
    main()
