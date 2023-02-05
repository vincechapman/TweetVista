from flask import Blueprint, render_template, request, session
from flask_login import login_required

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
def main():

    # from TLInterface.get_campaigns import get_all_campaigns
    #
    # campaigns = get_all_campaigns()

    return render_template('pages/dashboard.html')
