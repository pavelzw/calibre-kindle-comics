import os
from subprocess import Popen, PIPE, STDOUT

from calibre.ptempfile import PersistentTemporaryDirectory
from calibre.utils.zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


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
    print("Creating epub file.")
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
    print("Extracted kindlegen at", kindlegen_path)

    mobi_path = os.path.splitext(epub_path)[0] + ".mobi"
    print("MOBIPATH", mobi_path)

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
