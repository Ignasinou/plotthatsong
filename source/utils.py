import os
import shutil
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import wave
import logging
import colorlog
import time
import numpy as np
log = logging.getLogger("log_plotthatsong")
log.setLevel(logging.DEBUG)


def init_log():
    timestr = time.strftime("%Y%m%d_%H%M%S")
    log_filepath = f"log_{timestr}.txt"
    if os.path.exists(log_filepath):
        os.remove(log_filepath)
    fileHandler = logging.FileHandler(log_filepath)
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
    )
    log.addHandler(handler)
    log.addHandler(fileHandler)
    log.info(f"CREATED: Log file {log_filepath}.")


def add_titles(data):
    plt.title(
        f"{data['album']}\n"
        f"{data['artist']}",
        fontsize=20,
        loc='left',
        fontweight='bold',
        style='italic',
        y=1.02
    )

    plt.title(
        f"- {data['song_name']} -",
        fontsize=20,
        # loc='right',
        fontweight='bold',
        style='italic',
        y=1.05
    )

    plt.xlabel('Time (s)', fontsize=15, labelpad=20)
    plt.ylabel('Amplitude', fontsize=15, labelpad=20)


def read_audiofile(audio_wav, metadata):

    with wave.open(audio_wav, 'rb') as f:
        channels = f.getnchannels()
        num_frames = f.getnframes()
        audio_data = f.readframes(num_frames)
        sr = f.getframerate()

    audio_data = np.frombuffer(audio_data, dtype=np.int16)
    time_values = np.arange(0, num_frames) / sr
    max_abs_value = np.max(np.abs(audio_data))
    normalized_audio_data = audio_data / max_abs_value
    normalized_audio_data = normalized_audio_data[::metadata['downsampling_factor']]

    time_values = time_values[::metadata['downsampling_factor']]
    time_values = time_values + metadata['audio_start']

    if channels == 2:
        left_channel = normalized_audio_data[::2]
        right_channel = normalized_audio_data[1::2]
    else:
        left_channel = normalized_audio_data
        right_channel = None

    return time_values, right_channel, left_channel


def rm_and_create_dir(root, dest):
    fullpath_dir = os.path.join(root, dest)
    if os.path.exists(fullpath_dir):
        shutil.rmtree(fullpath_dir)
    os.makedirs(fullpath_dir)
    return fullpath_dir


def add_individual_legend(list_legends, legend_name):
    for leg in list_legends:
        if leg.get_label() != legend_name:
            leg.set_alpha(0)
        leg.set_label(" " * int(2 * len(leg.get_label())))
    return list_legends


def add_legend(name, color, lw, alpha):
    custom_lines = [Line2D([0], [0], color=color, lw=lw, alpha=alpha, label=name)]
    return custom_lines[0]


def create_legend(list_legends, color_div=None):
    # Envelope:
    name = 'Envelope'
    color = "black"
    env_legend = add_legend(name, color, 0.8, 1)
    list_legends.append(env_legend)

    # AmpR:
    name = 'Right channel'
    color = "teal"
    r_legend = add_legend(name, color, 1.5, 1)
    list_legends.append(r_legend)

    # AmpL:
    name = 'Left channel'
    color = "coral"
    l_legend = add_legend(name, color, 1.5, 1)
    list_legends.append(l_legend)

    # Beats
    name = 'Beats'
    color = "indigo"
    b_legend = add_legend(name, color, 2, 0.4)
    list_legends.append(b_legend)

    # Beats
    name = 'Spectrogram'
    color = (0, 0, 0, 0.3)
    b_legend = add_legend(name, color, 2, 0.4)
    list_legends.append(b_legend)

    # Spect
    if color_div is not None:
        for col_div in range(1, color_div):
            name = f"{-1 * (col_div - 1) * 20}dB to -{col_div * 20}dB"
            c = (-(col_div - 3) * 85) / 255
            color = (c, c, c)
            b_legend = add_legend(name, color, 1.5, 1)
            list_legends.append(b_legend)
    return list_legends
