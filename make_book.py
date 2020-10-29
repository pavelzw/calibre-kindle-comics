import os
import random
import sys
from multiprocessing import Pool
from shutil import copytree, move, rmtree

from calibre.ebooks.metadata import MetaInformation
from calibre.gui2 import Dispatcher
from calibre.ptempfile import PersistentTemporaryDirectory
from calibre.utils.logging import INFO
global _log, _options


def make_book(options, comic_file, log):
    global _log, _options
    _options = options
    print(options)
    _log = log
    log.prints(INFO, "Extracting images.")
    path = get_work_folder(comic_file)
    log.prints(INFO, "Processing images.")
    img_directory_processing(path)


def get_work_folder(comic_file):
    from calibre.ebooks.comic.input import extract_comic
    target_dir = extract_comic(comic_file)
    _log.prints(INFO, "Extracted images into " + target_dir)

    # move file structure up
    subdirectories = os.listdir(target_dir)
    if 'ComicInfo.xml' in subdirectories:
        subdirectories.remove('ComicInfo.xml')
    if len(subdirectories) == 1 and os.path.isdir(os.path.join(target_dir, subdirectories[0])):
        for f in os.listdir(os.path.join(target_dir, subdirectories[0])):
            move(os.path.join(target_dir, subdirectories[0], f), target_dir)
        os.rmdir(os.path.join(target_dir, subdirectories[0]))

    new_path = PersistentTemporaryDirectory(suffix='_oebps')
    copytree(target_dir, os.path.join(new_path, 'OEBPS', 'Images'))
    rmtree(target_dir)
    _log.prints(INFO, "Moved images to structure in " + new_path)

    return new_path


def img_directory_processing(path):
    img_metadata = {}
    img_old = []
    work = []
    page_number = 0
    for dir_path, _, filenames in os.walk(path):
        for file in filenames:
            page_number += 1
            work.append([file, dir_path])
    if len(work) > 0:
        for i in work:
            _log.prints(INFO, "Processing file", i[0])
            output = img_file_processing(i[0], i[1])

            for page in output:
                # additional metadata for the page (rotated, margins)
                img_metadata[page[0]] = page[1]
                # remove old images
                if page[2] not in img_old:
                    img_old.append(page[2])
        for file in img_old:
            os.remove(file)
    else:
        rmtree(os.path.join(path, '..', '..'), True)
        raise UserWarning("Source directory is empty.")


def img_file_processing(file, dir_path):
    from calibre_plugins.kindle_comics.image import ComicPageParser, ComicPage
    output = []
    work_img = ComicPageParser((dir_path, file), _options)
    for i in work_img.payload:
        img = ComicPage(_options, *i)
        if _options['cropping'] == 2 and not _options['webtoon']:
            img.cropPageNumber(_options['croppingp'])
        if _options['cropping'] > 0 and not _options['webtoon']:
            img.cropMargin(_options['croppingp'])
        print("Autocontrast")
        img.autocontrastImage()
        print("Resize")
        img.resizeImage()
        if _options['forcepng'] and not _options['forcecolor']:
            img.quantizeImage()
        output.append(img.saveToDir())
    return output
