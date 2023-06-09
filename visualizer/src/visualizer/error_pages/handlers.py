"""handlers for error pages
"""
from flask import Blueprint, render_template
from visualizer import log

error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(403)
def error_403(e):
    """403 error handler
    """
    log.error('access forbidden')
    return render_template('error_pages/403.html'), 403


@error_pages.app_errorhandler(404)
def error_404(e):
    """404 error handler
    """
    log.error('page not found')
    return render_template('error_pages/404.html'), 404


@error_pages.app_errorhandler(500)
def error_500(e):
    """500 error handler
    """
    log.error('internal server error')
    return render_template('error_pages/500.html'), 500


# @app.errorhandler(HTTPError)
# def handle_httperror(exception):
#     """hanldes HTTPErrors for requests when raise_for_status exception
#     is catched
#     Args:
#         exception (class): HTTPError exception class

#     Returns:
#         json: error message from hotspots API in json format
#     """
#     return jsonify({"message": f"Hotspots-API: {exception.args[0]}"}), 500
