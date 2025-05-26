#!/bin/env python
import os
import pytest
import logging
from typing import Iterable
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
Log = logging.getLogger(__name__)
FILENAME = 'example'
MD = os.path.join('tests', f'{FILENAME}.md')
DOCX = os.path.join('tests', f'{FILENAME}.docx')
def no_ext(path: str): return os.path.splitext(path)[0]
def dir_filename(path: str): return os.path.dirname(path), os.path.basename(path)


def unzip(zip: str):
    from zipfile import ZipFile
    To = no_ext(zip)
    with ZipFile(zip, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(To)
    Log.info(f"📚 Unzip {zip} to {To} 📂")
    return To


def pandoc(input: str, output: str, yaml: str | None = None, args=[], **kwargs):
    '''return output file path, would ***raise ChildProcessError*** if failed

    Args:
        input: input file path
        output: output file path, **MUST** follow extension name like `.docx`/`.md`...
        yaml: yaml config file path
        diy (bool): generate default pandoc `diy_template.EXT`
        args (list): additional arguments for pandoc command
    '''
    EXT = output.split('.')[-1].lower()
    _defaults = f'--defaults={yaml}' if yaml else ''
    Dir, basename = dir_filename(input)

    # eg: input="in.md", _res_path="./in" if exists else "./"
    _res_path = os.path.join(Dir, no_ext(os.path.basename(input)))
    if not os.path.exists(_res_path):
        _res_path = Dir

    _res_path = f"--resource-path='{_res_path}'" if _res_path else ''
    cmd = f"pandoc {_defaults} {_res_path} '{input}' -o '{output}' "
    for k, v in kwargs.items():
        if k and v:
            if isinstance(v, Iterable) and not isinstance(v, str):
                _s = f'--{k}='
                _s += f' --{k}='.join(v)
            else:
                _s = f'--{k}={v}'
            args.append(_s)
    cmd += ' '.join(args)
    Log.info(f"📜 {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        raise ChildProcessError(f"❌ Pandoc failed with error code {ret}")
    return output


def test_md_to_docx():
    os.environ['DEBUG'] = '1'
    output = pandoc(MD, DOCX, filter=[
        'pandoc-plot', 'pandoc-figure-caption-patch', 'pandoc-crossref'
    ])
    # To = unzip(output)
    # xml = os.path.join(To, 'word', 'document.xml')
    assert output


if __name__ == '__main__':
    test_md_to_docx()
