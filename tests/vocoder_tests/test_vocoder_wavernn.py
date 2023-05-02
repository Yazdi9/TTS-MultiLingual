import random

import numpy as np
import torch

from TTS.vocoder.configs import WavernnConfig
from TTS.vocoder.models.wavernn import Wavernn, WavernnArgs


def test_wavernn():
    config = WavernnConfig()
    config.model_args = WavernnArgs(
        rnn_dims=512,
        fc_dims=512,
        mode="mold",
        mulaw=False,
        pad=2,
        use_aux_net=True,
        use_upsample_net=True,
        upsample_factors=[4, 8, 8],
        feat_dims=80,
        compute_dims=128,
        res_out_dims=128,
        num_res_blocks=10,
    )
    config.audio.hop_length = 256
    config.audio.sample_rate = 2048

    dummy_x = torch.rand((2, 1280))
    dummy_m = torch.rand((2, 80, 9))
    y_size = random.randrange(20, 60)
    dummy_y = torch.rand((80, y_size))

    # mode: mold
    model = Wavernn(config)
    output = model(dummy_x, dummy_m)
    assert np.all(output.shape == (2, 1280, 30)), output.shape

    # mode: gauss
    config.model_args.mode = "gauss"
    model = Wavernn(config)
    output = model(dummy_x, dummy_m)
    assert np.all(output.shape == (2, 1280, 2)), output.shape

    # mode: quantized
    config.model_args.mode = 4
    model = Wavernn(config)
    output = model(dummy_x, dummy_m)
    assert np.all(output.shape == (2, 1280, 2**4)), output.shape
    output = model.inference(dummy_y, True, 5500, 550)
    assert np.all(output.shape == (256 * (y_size - 1),))
