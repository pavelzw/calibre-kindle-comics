__license__ = "ISC"
__copyright__ = "2012-2014, Ciro Mattia Gonano <ciromattia@gmail.com>, " \
                "2013-2019 Paweł Jastrzębski <pawelj@iosphe.re>"

from hashlib import md5


def md5_checksum(path):
    with open(path, 'rb') as fh:
        m = md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
