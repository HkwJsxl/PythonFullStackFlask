from flask import Flask, render_template

app = Flask(__name__)


@app.before_request
def before():
    print('before')


@app.after_request
def after(response):
    print('after')
    return response


@app.before_first_request
def first():
    print('first')


@app.teardown_request
def teardown(*args, **kwargs):
    # print('teardown', args)
    # print('teardown', kwargs)
    print('teardown')


@app.errorhandler(404)
def error_404(*args, **kwargs):
    print('errorhandler404', args)
    # print('errorhandler404', kwargs)
    return render_template('errors.html', message=args[0])


@app.template_global()
def a(a1, a2):
    return a1 + a2


@app.template_filter()
def b(a1, a2, a3):
    return a1 + a2 + a3


if __name__ == '__main__':
    app.run()
