
from flask import Flask, render_template
app = Flask(__name__)

app.secret_key = 'this is what the secrect key is eragaerhrhthsdhhasdfhafdhqaerhaerhmakirgmlkargnhka6841jdf4urj5ldrbnlva'

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app




import NoteTakingAppProject.views


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return 'Could not find what you were looking for', 404
@app.errorhandler(500)
def not_found(error):
    return 'Could not find what you were looking for', 500