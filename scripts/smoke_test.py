#!/usr/bin/env python3
"""
End-to-end checks against a running stack, through nginx (Python standard library only).

  python3 scripts/smoke_test.py check            full smoke test; prints the created ids as JSON
  python3 scripts/smoke_test.py marker <title>   create a project with that title
  python3 scripts/smoke_test.py titles           print all project titles as JSON
  python3 scripts/smoke_test.py download <id>    download an attachment, print its SHA-256

Environment: BASE_URL (default http://localhost), DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD.
Exits non-zero on the first failed check.
"""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
import uuid

BASE = os.environ.get('BASE_URL', 'http://localhost').rstrip('/')


def request(method, path, body=None, token=None, headers=None, raw=False):
    headers = dict(headers or {})
    data = None
    if body is not None and not isinstance(body, bytes):
        data = json.dumps(body).encode()
        headers['Content-Type'] = 'application/json'
    elif body is not None:
        data = body
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            return response.status, response.headers, content if raw else (json.loads(content) if content else None)
    except urllib.error.HTTPError as error:
        content = error.read()
        return error.code, error.headers, content


def expect(condition, message):
    if not condition:
        print(f'FAIL: {message}', file=sys.stderr)
        sys.exit(1)
    print(f'ok    {message}', file=sys.stderr)


def login():
    status, _, data = request('POST', '/api/token/', {
        'email': os.environ['DJANGO_SUPERUSER_EMAIL'], 'password': os.environ['DJANGO_SUPERUSER_PASSWORD'],
    })
    expect(status == 200, 'superuser can log in')
    return data['access']


def multipart(fields, file_field, filename, content):
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'
        f'Content-Type: application/octet-stream\r\n\r\n'.encode() + content + b'\r\n'
    )
    parts.append(f'--{boundary}--\r\n'.encode())
    return b''.join(parts), f'multipart/form-data; boundary={boundary}'


def check():
    status, headers, data = request('GET', '/api/health/')
    expect(status == 200 and data == {'status': 'ok'}, 'health endpoint through nginx')
    expect(bool(headers.get('X-Request-ID')), 'responses carry a request id')

    status, headers, page = request('GET', '/', raw=True)
    expect(status == 200 and b'id="root"' in page, 'SPA is served')
    expect(headers.get('X-Frame-Options') == 'DENY', 'SPA has security headers')

    status, _, _ = request('GET', '/api/projects/')
    expect(status == 401, 'API rejects anonymous requests')

    token = login()
    status, _, project = request('POST', '/api/projects/', {'title': 'Smoke test project'}, token)
    expect(status == 201, 'create project')
    status, _, experiment = request('POST', '/api/experiments/', {'project': project['id'], 'title': 'Smoke test'}, token)
    expect(status == 201, 'create experiment')

    content = b'<svg onload="alert(1)">smoke ' + uuid.uuid4().hex.encode() + b'</svg>'
    body, content_type = multipart({'experiment': experiment['id']}, 'file', 'spectrum.svg', content)
    status, _, attachment = request('POST', '/api/attachments/', body, token, {'Content-Type': content_type})
    expect(status == 201, 'upload attachment through nginx')
    expect(attachment['sha256'] == hashlib.sha256(content).hexdigest(), 'server-side checksum matches')

    status, headers, downloaded = request('GET', attachment['download_url'], token=token, raw=True)
    expect(status == 200 and downloaded == content, 'download through nginx X-Accel-Redirect returns the file')
    expect(headers.get('Content-Disposition', '').startswith('attachment'), 'download is never rendered inline')
    expect(headers.get('X-Content-Type-Options') == 'nosniff', 'nginx keeps nosniff on X-Accel downloads')
    expect('sandbox' in headers.get('Content-Security-Policy', ''), 'nginx keeps the sandbox CSP on X-Accel downloads')
    expect('X-Accel-Redirect' not in headers, 'internal redirect header is not exposed')

    status, _, _ = request('GET', attachment['download_url'], raw=True)
    expect(status == 401, 'anonymous download is rejected')
    status, _, _ = request('GET', f"/protected-attachments/attachments/{experiment['id']}/{attachment['id']}", raw=True)
    expect(status == 404, 'internal attachment location is not reachable directly')

    print(json.dumps({'project': project['id'], 'experiment': experiment['id'], 'attachment': attachment['id'],
                      'sha256': attachment['sha256']}))


def marker(title):
    status, _, _ = request('POST', '/api/projects/', {'title': title}, login())
    expect(status == 201, f'create project {title!r}')


def titles():
    status, _, data = request('GET', '/api/projects/?page_size=500', token=login())
    expect(status == 200, 'list projects')
    print(json.dumps(sorted(p['title'] for p in data['results'])))


def download(attachment_id):
    status, _, content = request('GET', f'/api/attachments/{attachment_id}/download/', token=login(), raw=True)
    expect(status == 200, 'download attachment')
    print(hashlib.sha256(content).hexdigest())


if __name__ == '__main__':
    command, *args = sys.argv[1:] or ['check']
    {'check': check, 'marker': marker, 'titles': titles, 'download': download}[command](*args)
