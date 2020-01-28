from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    client_ip = request.headers.get('X-Real-IP')
    if 'ref.' in request.host_url:
        print(f'Request reference from {client_ip}')
        return render_template('ref.html')
    else:
        print(f'Request index from {client_ip}')
        return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=33225, debug=True)
