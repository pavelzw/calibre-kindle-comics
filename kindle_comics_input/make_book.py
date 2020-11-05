import os
import time
from re import sub, split
from shutil import copytree, move, rmtree

from calibre.ptempfile import PersistentTemporaryDirectory
from calibre.utils.logging import INFO
from calibre.utils.short_uuid import uuid4
from calibre_plugins.kindle_comics.build_file import build_epub

global _log, _options


def make_book(options, comic_file, log):
    global _log, _options
    _options = options
    print(options)
    _log = log
    log.prints(INFO, "Extracting images.")
    path = get_work_folder(comic_file)
    image_path = os.path.join(path, "OEBPS", "Images")
    log.prints(INFO, "Processing images.")
    img_directory_processing(image_path)
    chapter_names = sanitize_tree(image_path)

    options['uuid'] = str(uuid4())
    _log.prints(INFO, "Creating EPUB file...")
    return build_epub(path, options, chapter_names)


    # filepath.append(getOutputFilename(source, options.output, '.epub', ''))
    # makeZIP(tome + '_comic', tome, True)
    # move(tome + '_comic.zip', filepath[-1])
    # rmtree(tome, True)
    # if GUI:
    #     GUI.progressBarTick.emit('tick')


def sanitize_tree(file_tree):
    _log.prints(INFO, "Sanitizing tree...")
    chapter_names = {}
    for root, dirs, files in os.walk(file_tree, False):
        # slugify files
        for name in files:
            split_name = os.path.splitext(name)
            slugified = _slugify(split_name[0], False)
            while os.path.exists(os.path.join(root, slugified + split_name[1])) \
                    and split_name[0].upper() != slugified.upper():
                slugified += "A"
            new_key = os.path.join(root, slugified + split_name[1])
            key = os.path.join(root, name)
            if key != new_key:
                os.replace(key, new_key)
        # slugify directories
        for name in dirs:
            tmp_name = name
            slugified = _slugify(name, True)
            while os.path.exists(os.path.join(root, slugified)) and name.upper() != slugified.upper():
                slugified += "A"
            chapter_names[slugified] = tmp_name
            new_key = os.path.join(root, slugified)
            key = os.path.join(root, name)
            if key != new_key:
                os.replace(key, new_key)
    return chapter_names


def _slugify(value, is_dir):
    from calibre_plugins.kindle_comics.kindle_comic_lib import slugify
    if is_dir:
        value = slugify(value, regex_pattern=r'[^-a-z0-9_\.]+').strip('.')
    else:
        value = slugify(value).strip('.')
    value = sub(r'0*([0-9]{4,})', r'\1', sub(r'([0-9]+)', r'0000\1', value, count=2))
    return value


def get_work_folder(comic_file):
    from calibre.ebooks.comic.input import extract_comic
    target_dir = extract_comic(comic_file)
    _log.prints(INFO, "Extracted images into " + target_dir)

    # move file structure up
    subdirectories = os.listdir(target_dir)

    # delete all not-images
    for file in os.listdir(target_dir):
        if os.path.isdir(os.path.join(target_dir, file)) \
                or file.lower().endswith('.png') \
                or file.lower().endswith('.jpg') \
                or file.lower().endswith('.jpeg') \
                or file.lower().endswith('.tif') \
                or file.lower().endswith('.tiff'):
            continue
        os.remove(os.path.join(target_dir, file))

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
    _options['imgMetadata'] = {}
    img_old = []
    work = []
    page_number = 0
    for dir_path, _, filenames in os.walk(path):
        for file in filenames:
            page_number += 1
            work.append([file, dir_path])
    if len(work) > 0:
        for i in work:
            _log.prints(INFO, "Processing file" + i[0])
            output = img_file_processing(i[0], i[1])

            for page in output:
                # additional metadata for the page (rotated, margins)
                _options['imgMetadata'][page[0]] = page[1]
                # remove old images
                if page[2] != page[3] and page[2] not in img_old:
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
        img.autocontrastImage()
        img.resizeImage()
        if _options['forcepng'] and not _options['forcecolor']:
            img.quantizeImage()
        output.append(img.saveToDir())
    return output
