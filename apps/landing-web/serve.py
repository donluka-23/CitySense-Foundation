"""Loopback-only static preview, no persistence, access logging or repository-root serving."""
import argparse
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent / 'dist'
PAGE_NAMES = ['index', 'partners', 'contact', 'privacy', 'terms', 'affiliate-disclosure']
ROUTES = {'/': ROOT / 'index.html', '/robots.txt': ROOT / 'robots.txt', '/sitemap.xml': ROOT / 'sitemap.xml'}
ROUTES.update({'/' + name + '.html': ROOT / (name + '.html') for name in PAGE_NAMES})
ROUTES.update({'/assets/' + name: ROOT / 'assets' / name for name in ['site.css', 'favicon.svg', 'batumi-480.webp', 'batumi-960.webp', 'batumi-1335.webp']})
CSP = "default-src 'self'; script-src 'none'; style-src 'self'; img-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"


class Handler(BaseHTTPRequestHandler):
    server_version = 'CitySenseLocalPreview'
    sys_version = ''
    protocol_version = 'HTTP/1.1'

    def log_message(self, *_args):
        pass

    def respond(self, code, body=b'', mime='text/plain; charset=utf-8'):
        self.send_response(code)
        for key, value in [('Content-Type', mime), ('Content-Length', str(len(body))), ('Cache-Control', 'no-store'), ('X-Content-Type-Options', 'nosniff'), ('Referrer-Policy', 'no-referrer'), ('Content-Security-Policy', CSP), ('X-Frame-Options', 'DENY'), ('Permissions-Policy', 'camera=(), microphone=(), geolocation=()'), ('X-Robots-Tag', 'noindex, nofollow'), ('Connection', 'close')]:
            self.send_header(key, value)
        self.end_headers()
        self.close_connection = True
        if self.command != 'HEAD':
            self.wfile.write(body)

    def do_GET(self):
        port = self.server.server_address[1]
        if self.headers.get('Host') not in {f'127.0.0.1:{port}', f'localhost:{port}'}:
            self.respond(403, b'Host refused'); return
        path = urlsplit(self.path).path
        file = ROUTES.get(path)
        if file is None:
            self.respond(404, b'Page not found'); return
        if not file.is_file():
            self.respond(503, b'Build the local website before previewing'); return
        mime = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
        if file.suffix == '.html':
            mime = 'text/html; charset=utf-8'
        elif file.suffix == '.css':
            mime = 'text/css; charset=utf-8'
        self.respond(200, file.read_bytes(), mime)

    def do_HEAD(self):
        self.do_GET()

    def reject_method(self):
        self.respond(405, b'Method not allowed')

    do_POST = reject_method
    do_PUT = reject_method
    do_PATCH = reject_method
    do_DELETE = reject_method
    do_OPTIONS = reject_method
    do_TRACE = reject_method


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4173)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        raise SystemExit('Port must be between 1024 and 65535')
    if not (ROOT / 'index.html').is_file():
        raise SystemExit('Run python apps/landing-web/build.py first')
    with ThreadingHTTPServer(('127.0.0.1', args.port), Handler) as server:
        print(f'CitySense local preview: http://127.0.0.1:{args.port}/ (not a production host)', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
