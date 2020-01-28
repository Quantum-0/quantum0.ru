from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    if 'ref.' in request.host_url:
        return render_template('ref.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=33225, debug=True)
