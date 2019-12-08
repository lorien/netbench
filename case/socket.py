import socket
import ssl
from io import BytesIO
import gzip

from util import run_threads, DEFAULT_HEADERS

GZIP_SIGNATURE = b'\x1f\x8b'


def worker(taskq):
    while True:
        try:
            url = taskq.pop()
        except IndexError:
            break
        else:
            scheme, rest = url.split('://', 1)
            hostname = rest.split('/')[0].split('?')[0]
            path = url.split(hostname, 1)[1]

            port = 443 if scheme == 'https' else 80
            ctx = ssl.create_default_context()

            with socket.create_connection((hostname, port)) as raw_sock:
                raw_sock.settimeout(30)
                if scheme == 'https':
                    sock = ctx.wrap_socket(raw_sock, server_hostname=hostname)
                else:
                    sock = raw_sock
                try:
                    sock.sendall(
                        b'GET %s HTTP/1.1\r\n'
                        b'Host: %s\r\n'
                        b'%s\r\n'
                        b'\r\n'
                        % (
                            path.encode(),
                            hostname.encode(),
                            ('\r\n'.join(
                                '%s: %s' % x for x in DEFAULT_HEADERS.items()
                            )).encode(),
                        )
                    )
                    inp = BytesIO()
                    while True:
                        data = sock.recv(2**16)
                        if data:
                            inp.write(data)
                        else:
                            break
                    data = inp.getvalue()
                    data_view = memoryview(data)
                    status_line = bytes(data_view[:data.index(b'\r\n')])
                    delimiter = b'\r\n\r\n'
                    split_pos = data.index(delimiter)
                    head = data_view[:split_pos]
                    body = data_view[(split_pos + len(delimiter)):]
                    if bytes(body[:2]) == GZIP_SIGNATURE:
                        body = gzip.decompress(body)
                    status = status_line.split(b' ')[1].decode()
                    print('%s => %d bytes' % (
                        status,
                        len(head) + len(delimiter) + len(body)
                    ))
                finally:
                    sock.close()


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
