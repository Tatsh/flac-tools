import logging
import os
import os.path
import re
import subprocess as sp

_log = logging.getLogger('flactools')


class TagDoesNotExistError(Exception):
    pass


def get_flac_tag(flac_filename, tag_name):
    """
    Raises TagDoesNotExistError if the tag is not found.
    """
    tag_name = tag_name.lower()
    cmd = [
        'metaflac',
        '--show-tag=%s' % (tag_name,),
        flac_filename,
    ]

    _log.debug(' '.join(cmd))

    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()

    output = p.stdout.read()
    output = output.decode('utf-8').strip()

    regex = r'^'
    regex += re.escape('%s=' % (tag_name,))

    _log.debug('Looking for %s' % (regex,))

    if re.match(regex, output, flags=re.IGNORECASE):
        try:
            found = re.split(regex,
                             output,
                             maxsplit=1,
                             flags=re.IGNORECASE)[1]
            return found.splitlines()[0]  # Return only first line
        except IndexError:
            return ''  # Assume the tag has an empty string as its value

    raise TagDoesNotExistError('Tag "%s" not found' % (tag_name,))


def convert_flac_to_wav(flac_file, dest=None):
    """
    Will raise IOError if the expected corresponding WAVE file is not
    created.
    """
    cmd = [
        'flac',
        '-f',
        '-d',
        flac_file,
    ]

    _log.info(' '.join(cmd))

    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()

    filename_without_ext, _ = os.path.splitext(flac_file)
    filename = '%s.wav' % (filename_without_ext,)

    with open(filename, 'rb'):
        pass

    if dest:
        os.rename(flac_file, dest)

    return filename
