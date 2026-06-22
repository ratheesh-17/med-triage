import urllib.request
import urllib.error
import json

BASE = 'http://127.0.0.1:8000'

def do_request(method, path, data=None, headers=None):
    url = BASE + path
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, method=method)
    req.add_header('Accept', 'application/json')
    if data is not None:
        req.add_header('Content-Type', 'application/json')
    if headers:
        for k,v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8')
            print(f"{method} {path} -> {resp.status}\n{body}\n")
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
        except:
            body = ''
        print(f"{method} {path} -> HTTP {e.code}\n{body}\n")
    except Exception as e:
        print(f"{method} {path} -> ERROR: {e}\n")

def run_tests():
    tests = [
        ('GET', '/'),
        ('GET', '/health'),
        ('POST', '/auth/login', {'phone': '9999999999'}),
        ('GET', '/chat'),
        ('GET', '/doctors/search?specialization=General%20Physician&user_lat=28.6&user_lng=77.2'),
        ('GET', '/appointments')
    ]

    for t in tests:
        method = t[0]
        path = t[1]
        data = t[2] if len(t) > 2 else None
        do_request(method, path, data)

if __name__ == '__main__':
    print('Running backend API smoke tests...')
    run_tests()
