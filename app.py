# py_ver == "3.6.9"
import flask
import validators
from flask import render_template



app = flask.Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    d = {"<": "&#x3C;", ">": "&#x3E;", '"': "&#x22;"}

    url = flask.request.path
    url_word = []
    for word in url:
        if word in d:
            url_word.append(d[word])
        else:
            url_word.append(word)
    new_url = ''.join(url_word)


    return """
          <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
          <title>404 Not Found</title>
          <h1>Not Found</h1>
          <p>The requested path <b>%s</b> was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
          """ % new_url

@app.route('/send_proxy_request')
def send_proxy_request():
    return """
            <html>
                <title>What to GET</title>
                <body>
                    <form action="/proxy_get">
                        Enter URL: <input name="url" type="text" />
                        <input name="submit" type="submit">
                    </form>
                </body>
            </html>
"""


import requests


@app.route('/proxy_get')
def proxy_get():
    url = flask.request.args.get('url')
    print(url)
    if url.startswith(('http://', 'https://')) and validators.url(url):
        result = requests.get(url)
        return "%s" % result.text
    else:
        return flask.redirect('/send_proxy_request')

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # only works in IE browser
    response.headers['X-Content-Security-Policy'] = "default-src 'self'"
    ##########################
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


if __name__ == '__main__':
    app.run()
