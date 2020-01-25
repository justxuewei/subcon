from flask import Flask, Response, request, abort
import requests
from requests.exceptions import MissingSchema
from io import StringIO
import re
from base64 import b64encode
from urllib.parse import quote

app = Flask(__name__)
encoding = 'utf-8'
unique_str = "djieHYnfe28f"


@app.route("/surge2ss", methods=['GET'])
def surge2ss():
    url = request.args.get('url')
    if not url:
        abort(403, 'Argument url is required.')

    r = None
    try:
        r = requests.get(url)
    except MissingSchema:
        abort(403, 'The format of url you provided is invalid.')

    surge_conf = r.content.decode(encoding)
    proxies = __surge_to_ss_parser(surge_conf)
    sssubs = __ss_to_sssubstr_parser(proxies)

    return Response(sssubs, content_type='text/plain')


def __surge_to_ss_parser(conf):
    buf = StringIO(conf)
    conf_readlines = buf.readlines()
    proxy_flag = False
    proxies = []
    for s in conf_readlines:
        # do nothing if this line has only "\n"
        if re.search(r'^[ ]*\r?\n', s):
            continue
        # check "[Proxy]" if proxy flag is False
        if not proxy_flag:
            proxy_result = re.search(r'\[Proxy\]', s)
            if proxy_result is not None:
                proxy_flag = True
        else:
            proxy_end_result = re.search(r'^\[.*\]', s)
            if proxy_end_result:
                break
            else:
                x = s.split('=', 1)
                # name handling
                name = re.sub(r'[ ]$', unique_str, x[0])
                info = x[1].replace(' ', '').replace('\r\n', '').replace('\n', '').split(',')

                if info[0] == 'ss' or info[0] == 'custom':
                    ss = ShadowSocks()
                    ss.name = name.replace(unique_str, '')
                    ss.host = info[1]
                    ss.port = info[2]
                    encrypt_method_arr = info[3].split('=')
                    ss.encrypt_method = encrypt_method_arr[1] if len(encrypt_method_arr) > 1 else encrypt_method_arr[0]
                    password_arr = info[4].split('=')
                    ss.password = password_arr[1] if len(password_arr) > 1 else password_arr[0]

                    proxies.append(ss)

    return proxies


def __ss_to_sssubstr_parser(ss):
    ss_subs = []
    for s in ss:
        encrypt_method_and_password = b64encode(('%s:%s' % (s.encrypt_method, s.password)).encode(encoding)) \
            .decode(encoding).replace('=', '')
        name_url_encoding = quote(s.name)
        ss_subs.append(
            'ss://%s@%s:%s#%s' % (encrypt_method_and_password, s.host, s.port, name_url_encoding)
        )
    ss_subs_str = '\n'.join(ss_subs)
    return b64encode(ss_subs_str.encode(encoding)).decode(encoding)


class ShadowSocks:

    def __init__(self):
        self._name = None
        self._host = None
        self._port = None
        self._encrypt_method = None
        self._password = None

    def __str__(self):
        return "[ShadowSocks] name: %s, host: %s, port: %s, encrypt_method: %s, password: %s" % (
            self.name, self.host, self.port, self.encrypt_method, self.password
        )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def encrypt_method(self):
        return self._encrypt_method

    @encrypt_method.setter
    def encrypt_method(self, med):
        self._encrypt_method = med

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password


if __name__ == "__main__":
    app.run(host='localhost', port=8080)
