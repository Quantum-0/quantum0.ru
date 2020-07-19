from flask import Flask, render_template, request, jsonify
import re, datetime
import http
from dateutil import tz
import random
from time import sleep
app = Flask(__name__)


@app.route('/')
def index():
    if 'quantum0' not in request.host_url:
        return render_template('nop.html')
    if 'ref.' in request.host_url:
        return render_template('ref.html')
    else:
        return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    ua = request.headers.get('User-Agent')
    if not 'Mozilla' in ua and not 'Chrome' in ua and not 'Safari' in ua:
        sleep(20)
        return jsonify({'success': random.choice([True, False, 'Yes', 'No', 'Lol']), 'login': random.choice(['administrator', 'admin', 'tvoya_mamka']), 'pass': random.choice(['qwertyzxc111!', 'kjkblbyf[eq'])}), 200
    else:
        sleep(3)
        return render_template('nop.html'), 404

def convert_time(dt):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Moscow')
    return dt.replace(tzinfo=from_zone).astimezone(to_zone)


@app.route('/logs/nginx')
def nginx_logs():
    logs = []
    log_parser = re.compile(r'\[(.+)\] ([\d\.]+) - "(.+)" "(.+)" "\d+" \d+ ".+" ".*"')
    with open('/var/log/nginx/access.log', 'r') as content_file:
        for number, line in enumerate(content_file):
            match = log_parser.match(line)
            if match is not None:
                time = datetime.datetime.strptime(match.group(1), '%d/%b/%Y:%H:%M:%S %z')
                ip = match.group(2)
                host = match.group(4)
                req = match.group(3)
                logs.append({'i': number, 'time': convert_time(time).strftime('%H:%M:%S %b, %d'), 'ip': ip, 'host': host, 'request': req})
    return render_template('nginx_logs_view.html', logs=logs)

@app.route('/logs/nginx/<int:id>')
def nginx_log_detailed(id):
    log_parser = re.compile(r'\[(.+)\] ([\d\.]+) - "(.+)" "(.+)" "(\d+)" (\d+) "(.+)" "(.*)"')
    with open('/var/log/nginx/access.log', 'r') as content_file:
        for number, line in enumerate(content_file):
            if number == id:
                match = log_parser.match(line)
                if match is not None:
                    time = datetime.datetime.strptime(match.group(1), '%d/%b/%Y:%H:%M:%S %z')
                    ip = match.group(2)
                    host = match.group(4)
                    req = match.group(3)
                    status = http.HTTPStatus(int(match.group(5)))
                    response_bytes = int(match.group(6))
                    http_ref = match.group(7)
                    user_agent = match.group(8)
                    return jsonify({'time': convert_time(time).strftime('%H:%M:%S %d/%b/%Y'), 'ip': ip, 'host': host,
                                    'request': req, 'code': f'HTTP {status} {status.name}',
                                    'response_bytes': response_bytes, 'http_ref': http_ref, 'user_agent': user_agent})
    return ''

if __name__ == '__main__':
    app.run('0.0.0.0', port=33225, debug=True)


request.getHeader("X-Forwarded-For");
