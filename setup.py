from __future__ import print_function
from distutils.core import setup
import subprocess as sp
import sys

github_url = 'https://github.com/Tatsh/flac-tools'

for name in ['metaflac', 'lame', 'flac', 'sox']:
    p = sp.Popen(['which', name], stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()

    if p.returncode != 0:
        print('Missing %s in PATH', file=sys.stderr)
        sys.exit(1)

setup(
    name='flac-tools',
    version='0.0.1',
    author='Andrew Udvare',
    author_email='audvare@gmail.com',
    url=github_url,
    packages=['flactools'],
    license='LICENSE.txt',
    description='Various FLAC utilities.',
    long_description='''Various FLAC utilities.

Note to package managers: please create symbolic links to flacted with the following names:

- flac-album
- flac-artist
- flac-genre
- flac-title
- flac-track
- flac-year

In the future this will be handled more normally with console_scripts.

See {url} for more information.'''.format(url=github_url),
    scripts=[
        'bin/flac2mp3',
        'bin/flacs2mp3-cue',
        'bin/flacted',
    ],
    install_requires=[
        'sh>=1.09',
        'six>=1.6.1',
    ],
)
