from flask import Blueprint, render_template, request, session
from flask_login import login_required

campaigns = Blueprint('campaigns', __name__, url_prefix='/campaigns')


@campaigns.route('/')
def main():

    from TLInterface.get_campaigns import get_all_campaigns

    campaigns = get_all_campaigns()

    return render_template('pages/campaigns.html', campaigns=campaigns)
