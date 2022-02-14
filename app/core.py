#non-user auth routes

from flask import render_template,request,Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def index():
  return render_template('index.html')

@core.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html') , 404

@core.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html') , 403