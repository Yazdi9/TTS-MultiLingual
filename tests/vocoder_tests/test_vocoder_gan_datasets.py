import os

import numpy as np
from torch.utils.data import DataLoader

from tests import get_tests_output_path, get_tests_path
from TTS.utils.audio import AudioProcessor
from TTS.vocoder.configs import BaseGANVocoderConfig
from TTS.vocoder.datasets.gan_dataset import GANDataset
from TTS.vocoder.datasets.preprocess import load_wav_data

file_path = os.path.dirname(os.path.realpath(__file__))
OUTPATH = os.path.join(get_tests_output_path(), "loader_tests/")
os.makedirs(OUTPATH, exist_ok=True)

C = BaseGANVocoderConfig()

test_data_path = os.path.join(get_tests_path(), "data/ljspeech/")
ok_ljspeech = os.path.exists(test_data_path)


def gan_dataset_case(
    batch_size, seq_len, hop_len, conv_pad, return_pairs, return_segments, use_noise_augment, use_cache, num_workers
):
    """Run dataloader with given parameters and check conditions"""
    ap = AudioProcessor(**C.audio)
    _, train_items = load_wav_data(test_data_path, 10)
    dataset = GANDataset(
        ap,
        train_items,
        seq_len=seq_len,
        hop_len=hop_len,
        pad_short=2000,
        conv_pad=conv_pad,
        return_pairs=return_pairs,
        return_segments=return_segments,
        use_noise_augment=use_noise_augment,
        use_cache=use_cache,
    )
    loader = DataLoader(
        dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True, drop_last=True
    )

    max_iter = 10
    count_iter = 0

    def check_item(feat, wav):
        """Pass a single pair of features and waveform"""
        feat = feat.numpy()
        wav = wav.numpy()
        expected_feat_shape = (batch_size, ap.num_mels, seq_len // hop_len + conv_pad * 2)

        # check shapes
        assert np.all(feat.shape == expected_feat_shape), f" [!] {feat.shape} vs {expected_feat_shape}"
        assert (feat.shape[2] - conv_pad * 2) * hop_len == wav.shape[2]

        # check feature vs audio match
        if not use_noise_augment:
            for idx in range(batch_size):
                audio = wav[idx].squeeze()
                feat = feat[idx]
                mel = ap.melspectrogram(audio)
                # the first 2 and the last 2 frames are skipped due to the padding
                # differences in stft
                max_diff = abs((feat - mel[:, : feat.shape[-1]])[:, 2:-2]).max()
                assert max_diff <= 1e-6, f" [!] {max_diff}"

    # return random segments or return the whole audio
    if return_segments:
        if return_pairs:
            for item1, item2 in loader:
                feat1, wav1 = item1
                feat2, wav2 = item2
                check_item(feat1, wav1)
                check_item(feat2, wav2)
                count_iter += 1
        else:
            for item1 in loader:
                feat1, wav1 = item1
                check_item(feat1, wav1)
                count_iter += 1
    else:
        for item in loader:
            feat, wav = item
            expected_feat_shape = (batch_size, ap.num_mels, (wav.shape[-1] // hop_len) + (conv_pad * 2))
            assert np.all(feat.shape == expected_feat_shape), f" [!] {feat.shape} vs {expected_feat_shape}"
            assert (feat.shape[2] - conv_pad * 2) * hop_len == wav.shape[2]
            count_iter += 1
            if count_iter == max_iter:
                break


def test_parametrized_gan_dataset():
    """test dataloader with different parameters"""
    params = [
        [32, C.audio["hop_length"] * 10, C.audio["hop_length"], 0, True, True, False, True, 0],
        [32, C.audio["hop_length"] * 10, C.audio["hop_length"], 0, True, True, False, True, 4],
        [1, C.audio["hop_length"] * 10, C.audio["hop_length"], 0, True, True, True, True, 0],
        [1, C.audio["hop_length"], C.audio["hop_length"], 0, True, True, True, True, 0],
        [1, C.audio["hop_length"] * 10, C.audio["hop_length"], 2, True, True, True, True, 0],
        [1, C.audio["hop_length"] * 10, C.audio["hop_length"], 0, True, False, True, True, 0],
        [1, C.audio["hop_length"] * 10, C.audio["hop_length"], 0, True, True, False, True, 0],
        [1, C.audio["hop_length"] * 10, C.audio["hop_length"], 0, False, True, True, False, 0],
        [1, C.audio["hop_length"] * 10, C.audio["hop_length"], 0, True, False, False, False, 0],
        [1, C.audio["hop_length"] * 10, C.audio["hop_length"], 0, True, False, False, False, 0],
    ]
    for param in params:
        print(param)
        gan_dataset_case(*param)
