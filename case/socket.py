import socket
import ssl
from io import BytesIO

from util import run_threads, DEFAULT_HEADERS


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
                    status_line = data[:data.index(b'\r\n')]
                    status = status_line.split(b' ')[1].decode()
                    print('%s => %d bytes' % (status, len(data)))
                finally:
                    sock.close()


def run(taskq, ncur):
    run_threads(taskq, ncur, worker)
