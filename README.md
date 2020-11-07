# Calibre Kindle Comics

[![GitHub release](https://img.shields.io/github/release/pavelzw/calibre-kindle-comics.svg)](https://github.com/pavelzw/calibre-kindle-comics/releases/latest)

**Calibre Kindle Comics** is a plugin for calibre that converts 
``.cbz`` and ``.cbr`` files into ``.mobi`` files that are 
optimized for Kindle devices. 

### Issues / new features
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

## INPUT FORMATS
Calibre Kindle Comics can convert ``.cbz`` and ``.cbr`` files at the moment.
It only converts to ``.mobi``, for other conversions like for example ``.epub``, 
the default calibre output plugins are being used.

## CREDITS
Calibre Kindle Comics is made by [Pavel Zwerschke](https://github.com/pavelzw).
I used some of the code by [Ciro Mattia Gonano](https://github.com/ciromattia) 
and [Paweł Jastrzębski](https://github.com/AcidWeb) from 
[Kindle Comic Converter](https://github.com/ciromattia/kcc) in the conversion 
of the comic files.

The plugin uses the ``image.py`` class from Alex Yatskov's [Mangle](https://github.com/FooSoft/mangle/) 
with subsequent [proDOOMman's](https://github.com/proDOOMman/Mangle) 
and [Birua's](https://github.com/Birua/Mangle) patches.