import json

from flask import Blueprint, request, jsonify

api_campaigns = Blueprint('api_campaigns', __name__, url_prefix='/api/campaigns')


@api_campaigns.route('/getCampaignData', methods=['POST'])
def get_campaign_data():

    print('api/getCampaignData called!')

    try:
        request_body = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return 'Failed to get stream.', 404
    else:
        campaign = request_body['campaign']

    from TLInterface.get_campaigns import get_campaign_data
    campaign_data = get_campaign_data(campaign)

    print(campaign_data)

    return jsonify(campaign_data)
