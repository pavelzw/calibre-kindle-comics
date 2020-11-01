import os
from re import split
from time import strftime, gmtime

from PIL import Image
from html import escape as html_escape
from calibre_plugins.kindle_comics.util import md5_checksum


def build_epub(path, options, chapter_names):
    from calibre_plugins.kindle_comics.image import Cover

    file_list = []
    chapter_list = []
    cover = None
    image_path = os.path.join(path, 'OEBPS', 'Images')
    text_path = os.path.join(path, 'OEBPS', 'Text')
    os.mkdir(os.path.join(path, 'OEBPS', 'Text'))

    # create style.css
    f = open(os.path.join(path, 'OEBPS', 'Text', 'style.css'), 'w', encoding='UTF-8')
    f.writelines(["@page {\n",
                  "margin: 0;\n",
                  "}\n",
                  "body {\n",
                  "display: block;\n",
                  "margin: 0;\n",
                  "padding: 0;\n",
                  "}\n"])
    if options['iskindle'] and options['panelview']:
        f.writelines(["#PV {\n",
                      "position: absolute;\n",
                      "width: 100%;\n",
                      "height: 100%;\n",
                      "top: 0;\n",
                      "left: 0;\n",
                      "}\n",
                      "#PV-T {\n",
                      "top: 0;\n",
                      "width: 100%;\n",
                      "height: 50%;\n",
                      "}\n",
                      "#PV-B {\n",
                      "bottom: 0;\n",
                      "width: 100%;\n",
                      "height: 50%;\n",
                      "}\n",
                      "#PV-L {\n",
                      "left: 0;\n",
                      "width: 49.5%;\n",
                      "height: 100%;\n",
                      "float: left;\n",
                      "}\n",
                      "#PV-R {\n",
                      "right: 0;\n",
                      "width: 49.5%;\n",
                      "height: 100%;\n",
                      "float: right;\n",
                      "}\n",
                      "#PV-TL {\n",
                      "top: 0;\n",
                      "left: 0;\n",
                      "width: 49.5%;\n",
                      "height: 50%;\n",
                      "float: left;\n",
                      "}\n",
                      "#PV-TR {\n",
                      "top: 0;\n",
                      "right: 0;\n",
                      "width: 49.5%;\n",
                      "height: 50%;\n",
                      "float: right;\n",
                      "}\n",
                      "#PV-BL {\n",
                      "bottom: 0;\n",
                      "left: 0;\n",
                      "width: 49.5%;\n",
                      "height: 50%;\n",
                      "float: left;\n",
                      "}\n",
                      "#PV-BR {\n",
                      "bottom: 0;\n",
                      "right: 0;\n",
                      "width: 49.5%;\n",
                      "height: 50%;\n",
                      "float: right;\n",
                      "}\n",
                      ".PV-P {\n",
                      "width: 100%;\n",
                      "height: 100%;\n",
                      "top: 0;\n",
                      "position: absolute;\n",
                      "display: none;\n",
                      "}\n"])
    f.close()

    for dir_path, dir_names, file_names in os.walk(image_path):
        chapter = False
        dir_names, file_names = walk_sort(dir_names, file_names)
        for file in file_names:
            file_list.append(build_html(dir_path, options, file, os.path.join(dir_path, file)))
            if not chapter:
                chapter_list.append((dir_path.replace('Images', 'Text'), file_list[-1][1]))
                chapter = True
            if cover is None: # add cover if not exists
                cover = os.path.join(image_path,
                                     'cover' + os.path.splitext(file_list[-1][1])[1].lower())
                options['covers'].append((Cover(os.path.join(file_list[-1][0], file_list[-1][1]), cover, options),
                                         options['uuid']))

    # Overwrite chapternames if tree is flat and ComicInfo.xml has bookmarks #todo necessary?
    # if not chapternames and options['chapters']:
    #     chapterlist = []
    #     globaldiff = 0
    #     for aChapter in options['chapters']:
    #         pageid = aChapter[0]
    #         for x in range(0, pageid + globaldiff + 1):
    #             if '-kcc-b' in filelist[x][1]:
    #                 pageid += 1
    #         if '-kcc-c' in filelist[pageid][1]:
    #             pageid -= 1
    #         filename = filelist[pageid][1]
    #         chapterlist.append((filelist[pageid][0].replace('Images', 'Text'), filename))
    #         chapternames[filename] = aChapter[1]
    #         globaldiff = pageid - (aChapter[0] + globaldiff)

    options['title'] = "TITLE" #todo
    build_ncx(path, options, chapter_list, chapter_names)
    build_nav(path, options, chapter_list, chapter_names)
    return build_opf(path, options, file_list, cover)


def build_html(path, options, img_file, img_file_path):
    img_path_md5 = md5_checksum(img_file_path)
    filename = os.path.splitext(img_file)
    device_res = options['profileData'][1]
    rotated_page = "Rotated" in options['imgMetadata'][img_path_md5]

    if "BlackBackground" in options['imgMetadata'][img_path_md5]:
        additional_style = 'background-color:#000000;'
    else:
        additional_style = ''
    postfix = ''
    backref = 1
    head = path
    while True:
        head, tail = os.path.split(head)
        if tail == 'Images':
            html_path = os.path.join(head, 'Text', postfix)
            break
        postfix = tail + "/" + postfix
        backref += 1
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    html_file = os.path.join(html_path, filename[0] + '.xhtml')
    img_size = Image.open(os.path.join(head, "Images", postfix, img_file)).size
    if options['hq']:
        img_size_frame = (int(img_size[0] // 1.5), int(img_size[1] // 1.5))
    else:
        img_size_frame = img_size
    f = open(html_file, "w", encoding='UTF-8')
    f.writelines(["<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
                  "<!DOCTYPE html>\n",
                  "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">\n",
                  "<head>\n",
                  "<title>", html_escape(filename[0]), "</title>\n",
                  "<link href=\"", "../" * (backref - 1), "style.css\" type=\"text/css\" rel=\"stylesheet\"/>\n",
                  "<meta name=\"viewport\" "
                  "content=\"width=" + str(img_size[0]) + ", height=" + str(img_size[1]) + "\"/>\n"
                  "</head>\n",
                  "<body style=\"" + additional_style + "\">\n",
                  "<div style=\"text-align:center;top:" + get_top_margin(device_res, img_size_frame) + "%;\">\n",
                  "<img width=\"" + str(img_size_frame[0]) + "\" height=\"" + str(img_size_frame[1]) + "\" ",
                  "src=\"", "../" * backref, "Images/", postfix, img_file, "\"/>\n</div>\n"])
    if options['iskindle'] and options['panelview']:
        if options['autoscale']:
            size = (get_panel_view_resolution(img_size, device_res))
        else:
            if options['hq']:
                size = img_size
            else:
                size = (int(img_size[0] * 1.5), int(img_size[1] * 1.5))
        if size[0] - device_res[0] < device_res[0] * 0.01:
            no_horizontal_pv = True
        else:
            no_horizontal_pv = False
        if size[1] - device_res[1] < device_res[1] * 0.01:
            no_vertical_pv = True
        else:
            no_vertical_pv = False
        x, y = get_panel_view_size(device_res, size)
        box_styles = {"PV-TL": "position:absolute;left:0;top:0;",
                     "PV-TR": "position:absolute;right:0;top:0;",
                     "PV-BL": "position:absolute;left:0;bottom:0;",
                     "PV-BR": "position:absolute;right:0;bottom:0;",
                     "PV-T": "position:absolute;top:0;left:" + x + "%;",
                     "PV-B": "position:absolute;bottom:0;left:" + x + "%;",
                     "PV-L": "position:absolute;left:0;top:" + y + "%;",
                     "PV-R": "position:absolute;right:0;top:" + y + "%;"}
        f.write("<div id=\"PV\">\n")
        if not no_horizontal_pv and not no_vertical_pv:
            if rotated_page:
                if options['righttoleft']:
                    order = [1, 3, 2, 4]
                else:
                    order = [2, 4, 1, 3]
            else:
                if options['righttoleft']:
                    order = [2, 1, 4, 3]
                else:
                    order = [1, 2, 3, 4]
            boxes = ["PV-TL", "PV-TR", "PV-BL", "PV-BR"]
        elif no_horizontal_pv and not no_vertical_pv:
            if rotated_page:
                if options['righttoleft']:
                    order = [1, 2]
                else:
                    order = [2, 1]
            else:
                order = [1, 2]
            boxes = ["PV-T", "PV-B"]
        elif not no_horizontal_pv and no_vertical_pv:
            if rotated_page:
                order = [1, 2]
            else:
                if options['righttoleft']:
                    order = [2, 1]
                else:
                    order = [1, 2]
            boxes = ["PV-L", "PV-R"]
        else:
            order = []
            boxes = []
        for i in range(0, len(boxes)):
            f.writelines(["<div id=\"" + boxes[i] + "\">\n",
                          "<a style=\"display:inline-block;width:100%;height:100%;\" class=\"app-amzn-magnify\" "
                          "data-app-amzn-magnify='{\"targetId\":\"" + boxes[i] +
                          "-P\", \"ordinal\":" + str(order[i]) + "}'></a>\n",
                          "</div>\n"])
        f.write("</div>\n")
        for box in boxes:
            f.writelines(["<div class=\"PV-P\" id=\"" + box + "-P\" style=\"" + additional_style + "\">\n",
                          "<img style=\"" + box_styles[box] + "\" src=\"", "../" * backref, "Images/", postfix,
                          img_file, "\" width=\"" + str(size[0]) + "\" height=\"" + str(size[1]) + "\"/>\n",
                          "</div>\n"])
    f.writelines(["</body>\n",
                  "</html>\n"])
    f.close()
    return path, img_file


def get_top_margin(device_res, size):
    y = int((device_res[1] - size[1]) / 2) / device_res[1] * 100
    return str(round(y, 1))


def get_panel_view_resolution(image_size, device_res):
    scale = float(device_res[0]) / float(image_size[0])
    return int(device_res[0]), int(scale * image_size[1])


def get_panel_view_size(device_res, size):
    x = int(device_res[0] / 2 - size[0] / 2) / device_res[0] * 100
    y = int(device_res[1] / 2 - size[1] / 2) / device_res[1] * 100
    return str(int(x)), str(int(y))


def build_ncx(dest_dir, options, chapters, chapter_names):
    title = options['title']
    ncx_file = os.path.join(dest_dir, 'OEBPS', 'toc.ncx')
    f = open(ncx_file, "w", encoding='UTF-8')
    f.writelines(["<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
                  "<ncx version=\"2005-1\" xml:lang=\"en-US\" xmlns=\"http://www.daisy.org/z3986/2005/ncx/\">\n",
                  "<head>\n",
                  "<meta name=\"dtb:uid\" content=\"urn:uuid:", options['uuid'], "\"/>\n",
                  "<meta name=\"dtb:depth\" content=\"1\"/>\n",
                  "<meta name=\"dtb:totalPageCount\" content=\"0\"/>\n",
                  "<meta name=\"dtb:maxPageNumber\" content=\"0\"/>\n",
                  "<meta name=\"generated\" content=\"true\"/>\n",
                  "</head>\n",
                  "<docTitle><text>", html_escape(title), "</text></docTitle>\n",
                  "<navMap>\n"])
    for chapter in chapters:
        folder = chapter[0].replace(os.path.join(dest_dir, 'OEBPS'), '').lstrip('/').lstrip('\\\\')
        filename = os.path.splitext(os.path.join(folder, chapter[1]))
        nav_id = folder.replace('/', '_').replace('\\', '_')
        if options['chapters']:
            title = chapter_names[chapter[1]]
            nav_id = filename[0].replace('/', '_').replace('\\', '_')
        elif os.path.basename(folder) != "Text":
            title = chapter_names[os.path.basename(folder)]
        f.write("<navPoint id=\"" + nav_id + "\"><navLabel><text>" +
                html_escape(title) + "</text></navLabel><content src=\"" + filename[0].replace("\\", "/") +
                ".xhtml\"/></navPoint>\n")
    f.write("</navMap>\n</ncx>")
    f.close()


def build_nav(dest_dir, options, chapters, chapter_names):
    title = options['title']
    nav_file = os.path.join(dest_dir, 'OEBPS', 'nav.xhtml')
    f = open(nav_file, "w", encoding='UTF-8')
    f.writelines(["<?xml version=\"1.0\" encoding=\"utf-8\"?>\n",
                  "<!DOCTYPE html>\n",
                  "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">\n",
                  "<head>\n",
                  "<title>" + html_escape(title) + "</title>\n",
                  "<meta charset=\"utf-8\"/>\n",
                  "</head>\n",
                  "<body>\n",
                  "<nav xmlns:epub=\"http://www.idpf.org/2007/ops\" epub:type=\"toc\" id=\"toc\">\n",
                  "<ol>\n"])
    for chapter in chapters:
        folder = chapter[0].replace(os.path.join(dest_dir, 'OEBPS'), '').lstrip('/').lstrip('\\\\')
        filename = os.path.splitext(os.path.join(folder, chapter[1]))
        if options['chapters']:
            title = chapter_names[chapter[1]]
        elif os.path.basename(folder) != "Text":
            title = chapter_names[os.path.basename(folder)]
        f.write("<li><a href=\"" + filename[0].replace("\\", "/") + ".xhtml\">" + html_escape(title) + "</a></li>\n")
    f.writelines(["</ol>\n",
                  "</nav>\n",
                  "<nav epub:type=\"page-list\">\n",
                  "<ol>\n"])
    for chapter in chapters:
        folder = chapter[0].replace(os.path.join(dest_dir, 'OEBPS'), '').lstrip('/').lstrip('\\\\')
        filename = os.path.splitext(os.path.join(folder, chapter[1]))
        if options['chapters']:
            title = chapter_names[chapter[1]]
        elif os.path.basename(folder) != "Text":
            title = chapter_names[os.path.basename(folder)]
        f.write("<li><a href=\"" + filename[0].replace("\\", "/") + ".xhtml\">" + html_escape(title) + "</a></li>\n")
    f.write("</ol>\n</nav>\n</body>\n</html>")
    f.close()


def build_opf(dest_dir, options, file_list, cover=None):
    title = options['title']
    opf_file = os.path.join(dest_dir, 'OEBPS', 'content.opf')
    device_res = options['profileData'][1]
    if options['righttoleft']:
        writingmode = "horizontal-rl"
    else:
        writingmode = "horizontal-lr"
    f = open(opf_file, "w", encoding='UTF-8')
    f.writelines(["<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
                  "<package version=\"3.0\" unique-identifier=\"BookID\" ",
                  "xmlns=\"http://www.idpf.org/2007/opf\">\n",
                  "<metadata xmlns:opf=\"http://www.idpf.org/2007/opf\" ",
                  "xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\n"])
    f.writelines(["<meta property=\"dcterms:modified\">" + strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()) + "</meta>\n",
                  "<meta name=\"cover\" content=\"cover\"/>\n"])
    if options['iskindle'] and options['profile'] != 'Custom':
        f.writelines(["<meta name=\"fixed-layout\" content=\"true\"/>\n",
                      "<meta name=\"original-resolution\" content=\"",
                      str(device_res[0]) + "x" + str(device_res[1]) + "\"/>\n",
                      "<meta name=\"book-type\" content=\"comic\"/>\n",
                      "<meta name=\"primary-writing-mode\" content=\"" + writingmode + "\"/>\n",
                      "<meta name=\"zero-gutter\" content=\"true\"/>\n",
                      "<meta name=\"zero-margin\" content=\"true\"/>\n",
                      "<meta name=\"ke-border-color\" content=\"#FFFFFF\"/>\n",
                      "<meta name=\"ke-border-width\" content=\"0\"/>\n"])
        if options['kfx']:
            f.writelines(["<meta name=\"orientation-lock\" content=\"none\"/>\n",
                          "<meta name=\"region-mag\" content=\"false\"/>\n"])
        else:
            f.writelines(["<meta name=\"orientation-lock\" content=\"portrait\"/>\n",
                          "<meta name=\"region-mag\" content=\"true\"/>\n"])
    else:
        f.writelines(["<meta property=\"rendition:orientation\">portrait</meta>\n",
                      "<meta property=\"rendition:spread\">portrait</meta>\n",
                      "<meta property=\"rendition:layout\">pre-paginated</meta>\n"])
    f.writelines(["</metadata>\n<manifest>\n<item id=\"ncx\" href=\"toc.ncx\" ",
                  "media-type=\"application/x-dtbncx+xml\"/>\n",
                  "<item id=\"nav\" href=\"nav.xhtml\" ",
                  "properties=\"nav\" media-type=\"application/xhtml+xml\"/>\n"])
    if cover is not None:
        filename = os.path.splitext(cover.replace(os.path.join(dest_dir, 'OEBPS'), '').lstrip('/').lstrip('\\\\'))
        if '.png' == filename[1]:
            mt = 'image/png'
        else:
            mt = 'image/jpeg'
        f.write("<item id=\"cover\" href=\"Images/cover" + filename[1] + "\" media-type=\"" + mt +
                "\" properties=\"cover-image\"/>\n")
    ref_list = []
    for path in file_list:
        folder = path[0].replace(os.path.join(dest_dir, 'OEBPS'), '').lstrip('/').lstrip('\\\\').replace("\\", "/")
        filename = os.path.splitext(path[1])
        print("UNIQUE ID\n\n\n", )
        unique_id = os.path.join(folder, filename[0]).replace('/', '_').replace('\\', '_')
        print("UNIQUE ID\n\n\n", unique_id)
        ref_list.append(unique_id)
        f.write("<item id=\"page_" + str(unique_id) + "\" href=\"" +
                folder.replace('Images', 'Text') + "/" + filename[0] +
                ".xhtml\" media-type=\"application/xhtml+xml\"/>\n")
        if '.png' == filename[1]:
            mt = 'image/png'
        else:
            mt = 'image/jpeg'
        f.write("<item id=\"img_" + str(unique_id) + "\" href=\"" + folder + "/" + path[1] + "\" media-type=\"" +
                mt + "\"/>\n")
    f.write("<item id=\"css\" href=\"Text/style.css\" media-type=\"text/css\"/>\n")
    if options['righttoleft']:
        f.write("</manifest>\n<spine page-progression-direction=\"rtl\" toc=\"ncx\">\n")
        page_side = "right"
    else:
        f.write("</manifest>\n<spine page-progression-direction=\"ltr\" toc=\"ncx\">\n")
        page_side = "left"
    if options['iskindle']:
        for entry in ref_list:
            if options['righttoleft']:
                if entry.endswith("-b"):
                    f.write("<itemref idref=\"page_" + entry + "\" linear=\"yes\" properties=\"page-spread-right\"/>\n")
                    page_side = "right"
                elif entry.endswith("-c"):
                    f.write("<itemref idref=\"page_" + entry + "\" linear=\"yes\" properties=\"page-spread-left\"/>\n")
                    page_side = "right"
                else:
                    f.write("<itemref idref=\"page_" + entry + "\" linear=\"yes\" properties=\"page-spread-" +
                            page_side + "\"/>\n")
                    if page_side == "right":
                        page_side = "left"
                    else:
                        page_side = "right"
            else:
                if entry.endswith("-b"):
                    f.write("<itemref idref=\"page_" + entry + "\" linear=\"yes\" properties=\"page-spread-left\"/>\n")
                    page_side = "left"
                elif entry.endswith("-c"):
                    f.write("<itemref idref=\"page_" + entry + "\" linear=\"yes\" properties=\"page-spread-right\"/>\n")
                    page_side = "left"
                else:
                    f.write("<itemref idref=\"page_" + entry + "\" linear=\"yes\" properties=\"page-spread-" +
                            page_side + "\"/>\n")
                if page_side == "right":
                    page_side = "left"
                else:
                    page_side = "right"
    else:
        for entry in ref_list:
            f.write("<itemref idref=\"page_" + entry + "\"/>\n")
    f.write("</spine>\n</package>\n")
    f.close()
    return opf_file


def walk_sort(dir_names, file_names):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in split('([0-9]+)', key)]
    dir_names.sort(key=lambda name: alphanum_key(name.lower()))
    file_names.sort(key=lambda name: alphanum_key(name.lower()))
    return dir_names, file_names
