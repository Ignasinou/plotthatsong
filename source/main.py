from CONF import *
from audio_processor import AudioProcessor
from audio_plotter import AudioPlotter
import logging
import argparse
from utils import init_log

log = logging.getLogger("log_plotthatsong")
log.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_fig_mode', help="Flag in order to preview the whole plot",
                        default=False, type=bool)
    args = parser.parse_args()
    init_log()

    metadata = {"song_name": song_name, "album": album, "artist": artist, 'audio_start': audio_chunk_start,
                'audio_end': audio_chunk_end, 'hop_length': hop_length, 'n_fft': n_fft,
                'plot_interval_secs': plot_interval_secs, 'downsampling_factor': downsampling_factor,
                'padding_end': padding_end, 'version': version_num, 'printnum': print_num}

    audio_processor = AudioProcessor(input_audio_wav, metadata)
    audio_processor.chunk_audio(audio_chunk_start, audio_chunk_end)
    audio_excerpt_filepath = audio_processor.get_output_chunk_file()
    metadata = audio_processor.get_general_data()

    audio_plotter = AudioPlotter(audio_excerpt_filepath, metadata, args.save_fig_mode)

    audio_plotter.plot_spect()
    audio_plotter.plot_audiowave()

    if not args.save_fig_mode:
        audio_plotter.mask_final_output()


if __name__ == "__main__":
    main()
