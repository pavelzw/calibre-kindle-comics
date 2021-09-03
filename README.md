# Calibre Kindle Comics

[![GitHub release](https://img.shields.io/github/release/pavelzw/calibre-kindle-comics.svg)](https://github.com/pavelzw/calibre-kindle-comics/releases/latest)

**Calibre Kindle Comics** is a plugin for calibre that converts 
``.cbz`` and ``.cbr`` files into ``.mobi`` files that are 
optimized for Kindle devices. 

### Issues/new features
If you have problems using this plugin or feature requests, please 
[file an issue](https://github.com/pavelzw/calibre-kindle-comics/issues/new).
If you can fix an open issue or want to add new features, 
fork the repository and create a pull request.

## Installation
You can find the latest release 
[here](https://github.com/pavelzw/calibre-kindle-comics/releases/latest).

Before you add the plugin to calibre, you need to add the 
KindleGen executable to the Kindle Comics Output plugin.
Since KindleGen is [no longer supported](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211) 
by Amazon, you need to download it from [archive.org](https://archive.org/details/kindlegen2.9):

- [Windows](https://archive.org/download/kindlegen2.9/kindlegen_win32_v2_9.zip/kindlegen.exe)
- [macOS](https://archive.org/download/kindlegen2.9/KindleGen_Mac_i386_v2_9.zip/kindlegen)
- [Linux](https://archive.org/download/kindlegen2.9/kindlegen_linux_2.6_i386_v2_9.tar.gz)

Extract the ``kindle_comics.zip`` and place the ``kindlegen.exe`` (Windows)
or ``kindlegen`` (Linux and macOS) into the ``Kindle Comics Output.zip`` file.

Then open calibre, go to ``Preferences`` > ``Plugins`` > ``Load plugin from file``
and select ``Kindle Comics Input.zip`` and then ``Kindle Comics Output.zip``.

## Input Formats
Calibre Kindle Comics can convert ``.cbz`` and ``.cbr`` files at the moment.
It only converts to ``.mobi``, for other conversions like for example ``.epub``, 
the default calibre output plugins are being used.

### How this plugin works
The Kindle Comics Input plugin acts as a converter from ``.cbz`` and ``.cbr`` 
to ``OEB``, that's how all Plugins of the type ``InputFormatPlugin`` work.
The Kindle Comics Output plugin then converts from the ``OEB`` format to 
``.mobi`` by first creating a ``.epub`` file and then executing KindleGen.
You still can convert from any other format to ``.epub``, Kindle Comics Output 
will use the default ``.mobi`` conversion plugin when the input is not by 
Kindle Comics Input.

I haven't figured out a way that Kindle Comics Input is only executed when 
the conversion is to ``.mobi``. That's why there may be strange results when 
converting to other formats or when viewing the comic file in the 
calibre ebook viewer. You may want to deactivate the plugin while converting 
non-comics to other file formats.

## Credits
Calibre Kindle Comics is made by [Pavel Zwerschke](https://github.com/pavelzw).
I used some of the code by [Ciro Mattia Gonano](https://github.com/ciromattia) 
and [Paweł Jastrzębski](https://github.com/AcidWeb) from 
[Kindle Comic Converter](https://github.com/ciromattia/kcc) in the conversion 
of the comic files.

The plugin uses the ``image.py`` class from Alex Yatskov's [Mangle](https://github.com/FooSoft/mangle/) 
with subsequent [proDOOMman's](https://github.com/proDOOMman/Mangle) 
and [Birua's](https://github.com/Birua/Mangle) patches.

## Considerations for MacOS
Get kindlegen by installing `kindle-comic-creator` with brew. The executable will be located at this location:
`/Applications/Kindle Comic Creator/Kindle Comic Creator.app/Contents/MacOS/kindlegen`. Otherwise you might run into
issues with `kindlegen` being only 32-bit compatible.
