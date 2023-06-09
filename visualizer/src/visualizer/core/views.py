"""The core view
"""
from flask import render_template, Blueprint, request, flash
import requests
from visualizer import app, log
from requests.exceptions import HTTPError

core_blueprint = Blueprint('core', __name__)


def flash_errors(form):
    """Flash errors for displaying as alerts in html templates"""
    for i in form.errors.values():
        flash(i[0])

@core_blueprint.route('/', methods=['GET'])
def home():
    """render home template
    """
    return render_template('home.html')



@core_blueprint.route('/hotspots/', methods=['GET'])
def get_hotposts():
    """render home template
    """
    args = request.args
    try:
        hotspots_url = f'{app.config["API_URL_BASE"]}/hotspots/'
        params = {
            'start_date': args['start_date'],
            'end_date': args['end_date'],
            'bounding_box': args['bounding_box'],
        }

        response = requests.get(
            hotspots_url,
            params=params,
            timeout=20)
        response.raise_for_status()

        
    # except HTTPError as error:
    except HTTPError as error:
        flash(error.response.text, 'warning')
        log.error(error)
        raise error

    hotspots_res = response.json()

    return hotspots_res