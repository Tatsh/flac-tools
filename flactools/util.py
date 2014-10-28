import logging
import subprocess as sp
import sys
import tempfile

_log = logging.getLogger('flactools')


def encode_wav_to_mp3(wav_filename, output_filename, lame_options=['-V', '0']):
    cmd = ['lame'] + lame_options + ['-S']  # Enforce no progress bar, etc
    cmd += [wav_filename, output_filename]

    _log.info(' '.join(cmd))

    stdout, stderr = sp.Popen(cmd,
                              stdout=sp.PIPE,
                              stderr=sp.PIPE).communicate()

    # stdout does not have anything
    _log.debug(stderr.decode('utf-8').strip())

    with open(output_filename, 'rb'):
        pass

    _log.info('Finished encoding to MP3')


def escape_quotes_for_cue(path):
    return path.replace('"', r'\"')


def merge_audio(list_of_files):
    merged_wav_output = tempfile.mkstemp(prefix='flactools.util.merge_audio__',
                                         suffix='__.wav')[1]
    sox_cmd = ['sox'] + list_of_files + [merged_wav_output]

    _log.info(' '.join(sox_cmd))
    p = sp.Popen(sox_cmd)
    p.wait()

    with open(merged_wav_output, 'rb'):
        pass

    return merged_wav_output


def get_logger(level=logging.ERROR, channel=None):
    logger = logging.getLogger('flactools')
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    if not channel:
        channel = logging.StreamHandler(sys.stderr)

    logger.setLevel(level)
    channel.setLevel(level)
    channel.setFormatter(formatter)
    logger.addHandler(channel)

    return logger
