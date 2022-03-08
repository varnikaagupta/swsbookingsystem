#non-user auth routes

from flask import render_template,request,Blueprint
from server import app
import os

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)


core = Blueprint('core',__name__)

app.register_blueprint(core)

@app.route('/')
def index():
  return render_template('index.html'), 200

@core.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html') , 404

@core.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html') , 403