import essentia.standard
import soundfile as sf
import pyloudnorm as pyln
import os
import shutil
import subprocess
import logging

log = logging.getLogger("log_plotthatsong")
log.setLevel(logging.DEBUG)


class AudioProcessor:
    def __init__(self, input_audio_wav, metadata):
        self.input_audio_wav = input_audio_wav
        self.metadata = metadata
        self.filename = self.input_audio_wav.split('/')[-1].split('.')[0]
        self.output_chunk_file = os.path.join(self.filename, self.filename + "_chunk.wav")

    def get_general_data(self):
        audio = essentia.standard.MonoLoader(filename=self.output_chunk_file)()
        rhythm_extractor = essentia.standard.RhythmExtractor2013(method="multifeature")
        bpm, ticks, confidence, estimates, beats_intervals = rhythm_extractor(audio)

        audio_data, rate = sf.read(self.output_chunk_file)
        meter = pyln.Meter(rate)
        loudness = meter.integrated_loudness(audio_data)
        self.metadata['bpm'] = bpm
        self.metadata['ticks'] = ticks
        self.metadata['loudness'] = loudness
        return self.metadata

    def chunk_audio(self, start_, end_):
        time_chunk = end_ - start_
        extension = self.input_audio_wav.split('/')[-1].split('.')[1]

        if os.path.exists(self.filename):
            shutil.rmtree(self.filename)
        os.mkdir(self.filename)

        wav_filename = f"{self.filename}.wav"
        log.info("Converting into WAV...")
        if extension != 'wav':
            subprocess.call(
                f"ffmpeg -i {self.input_audio_wav} {wav_filename} -y -loglevel error", shell=True)

        if os.path.exists(self.output_chunk_file):
            log.info("Skipping...")
        else:
            log.info("Retrieving the audio excerpt...")
            subprocess.call(
                f"ffmpeg -i {self.input_audio_wav} -ss {start_} -t {time_chunk} {self.output_chunk_file} -y -loglevel error",
                shell=True)

        self.metadata['filename'] = self.filename

    def get_output_chunk_file(self):
        return self.output_chunk_file

