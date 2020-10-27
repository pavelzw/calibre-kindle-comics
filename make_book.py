import os
from shutil import copytree, move, rmtree

from calibre.ptempfile import PersistentTemporaryDirectory
from calibre.utils.logging import INFO
from calibre_plugins.kindle_comics.corruption_detector import detect_corruption
global log


def make_book(comic_file, options, _log):
    global log
    log = _log
    log.prints(INFO, "Extracting images.")
    path = get_work_folder(comic_file)
    log.prints(INFO, "Checking images.")


def get_work_folder(comic_file):
    from calibre.ebooks.comic.input import extract_comic
    target_dir = extract_comic(comic_file)
    log.prints(INFO, "Extracted images into " + target_dir)

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
    log.prints(INFO, "Moved images to structure in " + new_path)
    return new_path

