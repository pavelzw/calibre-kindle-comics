import os
from subprocess import Popen, PIPE, STDOUT

from calibre.ptempfile import PersistentTemporaryDirectory
from calibre.utils.zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


def write_metadata_to_opf(opf_path, metadata):
    metadata_str = _get_metadata_str(metadata)

    with open(opf_path, "r") as in_file:
        buf = in_file.readlines()

    with open(opf_path, "w") as out_file:
        for line in buf:
            if line.startswith("<metadata"):
                line = line + metadata_str
            out_file.write(line)


def _get_metadata_str(metadata):
    title = metadata['title'][0] if len(metadata['title']) > 0 else None
    creators = metadata['creator']
    contributors = metadata['contributors']
    timestamp = metadata['timestamp'][0] if len(metadata['timestamp']) > 0 else None
    identifiers = metadata['identifier']
    title_sort = metadata['title_sort'][0] if len(metadata['title_sort']) > 0 else None
    description = metadata['description'][0] if len(metadata['description']) > 0 else None
    publishers = metadata['publisher']
    series = metadata['series'][0] if len(metadata['series']) > 0 else None
    series_index = metadata['series_index'][0] if len(metadata['series_index']) > 0 else None
    rating = metadata['rating'][0] if len(metadata['rating']) > 0 else None
    subjects = metadata['subject']
    date = metadata['date'][0] if len(metadata['date']) > 0 else None
    languages = metadata['language']
    metadata_str = ""
    if title is not None:
        metadata_str += _get_single_metadata_str(title)
    else:  # kindlegen needs dc:title
        metadata_str += "<dc:title>NO_TITLE</dc:title>"
    for creator in creators:
        metadata_str += _get_single_metadata_str(creator)
    for contributor in contributors:
        metadata_str += _get_single_metadata_str(contributor)
    if timestamp is not None:  # todo possible?
        metadata_str += _get_single_metadata_str(timestamp)
    for identifier in identifiers:
        metadata_str += _get_single_metadata_str(identifier)
    if title_sort is not None:
        metadata_str += _get_single_metadata_str(title_sort)
    if description is not None:
        metadata_str += _get_single_metadata_str(description)
    for publisher in publishers:
        metadata_str += _get_single_metadata_str(publisher)
    if series is not None:  # todo possible?
        metadata_str += _get_single_metadata_str(series)
    if series_index is not None:  # todo possible?
        metadata_str += _get_single_metadata_str(series_index)
    if rating is not None:
        metadata_str += _get_single_metadata_str(rating)
    for subject in subjects:
        metadata_str += _get_single_metadata_str(subject)
    if date is not None:
        metadata_str += _get_single_metadata_str(date)
    for language in languages:
        metadata_str += _get_single_metadata_str(language)
    if len(languages) == 0: # kindlegen needs dc:language
        metadata_str += "<dc:language>en-US</dc:language>"
    return metadata_str


def _get_single_metadata_str(item):
    name = item.name[item.name.find("}") + 1:]  # remove {...}
    metadata_str = "<dc:" + name
    for key, attribute in item.attrib.items():
        key = key[key.find("}") + 1:]  # remove {...}
        metadata_str += " opf:" + key + "=\"" + attribute + "\""
    metadata_str += ">" + item.content + "</dc:" + name + ">\n"
    return metadata_str


def build_meta_inf(dest_dir):
    os.mkdir(os.path.join(dest_dir, 'META-INF'))
    f = open(os.path.join(dest_dir, 'META-INF', 'container.xml'), 'w', encoding='UTF-8')
    f.writelines(["<?xml version=\"1.0\"?>\n",
                  "<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">\n",
                  "<rootfiles>\n",
                  "<rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>\n",
                  "</rootfiles>\n",
                  "</container>"])
    f.close()


def make_zip(zipfile_name, base_dir):
    zipfile_name = os.path.abspath(zipfile_name) + '.epub'
    zip_output = ZipFile(zipfile_name, 'w', ZIP_DEFLATED)
    zip_output.writestr('mimetype', 'application/epub+zip', ZIP_STORED)
    for dir_path, _, file_names in os.walk(base_dir):
        for name in file_names:
            path = os.path.normpath(os.path.join(dir_path, name))
            aPath = os.path.normpath(os.path.join(dir_path.replace(base_dir, ''), name))
            if os.path.isfile(path):
                zip_output.write(path, aPath)
    zip_output.close()
    return zipfile_name


def make_mobi(epub_path):
    # copy kindlegen to destination
    plugin_path = os.path.join(__file__, "..")
    plugin_zip = ZipFile(plugin_path)
    kindlegen_path = PersistentTemporaryDirectory("_kindlegen")
    plugin_zip.extract("kindlegen.exe", kindlegen_path)
    kindlegen_path = os.path.join(kindlegen_path, "kindlegen.exe")

    mobi_path = os.path.splitext(epub_path)[0] + ".mobi"

    # execute kindlegen
    # todo make pretty with return code
    kindlegen_error_code = 0
    kindlegen_error = ''
    try:
        if os.path.getsize(epub_path) < 629145600:
            output = Popen(kindlegen_path + ' -dont_append_source -locale en "' + epub_path + '"',
                           stdout=PIPE, stderr=STDOUT, stdin=PIPE, shell=True)
            for line in output.stdout:
                line = line.decode('utf-8')
                # ERROR: Generic error
                if "Error(" in line:
                    kindlegen_error_code = 1
                    kindlegen_error = line
                # ERROR: EPUB too big
                if ":E23026:" in line:
                    kindlegen_error_code = 23026
                if kindlegen_error_code > 0:
                    break
                if ":I1036: Mobi file built successfully" in line:
                    output.terminate()
        else:
            # ERROR: EPUB too big
            kindlegen_error_code = 23026
        return [kindlegen_error_code, kindlegen_error, mobi_path]
    except Exception as err:
        # ERROR: KCC unknown generic error
        kindlegen_error_code = 1
        kindlegen_error = format(err)
        return [kindlegen_error_code, kindlegen_error, None]
