import json
import logging

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


@api_campaigns.route('/startStopCampaign', methods=['POST'])
def start_stop_campaign():

    print('POST api/campaigns/startStopCampaign')

    try:
        request_body = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return 'Failed to get stream.', 404
    else:
        campaign_id = request_body['campaignID']
        campaign_name = request_body['campaignName']
        start_or_stop = request_body['start_or_stop']

    from TLInterface import get_web_connection
    wc = get_web_connection()

    if start_or_stop == 'start':
        response = wc.start_campaign_feed(
            campaign_id=campaign_id,
            campaign_name=campaign_name
        )
        logging.info(f'Campaign {campaign_id} ({campaign_name}) started.')
    else:
        response = wc.stop_campaign_feed(
            campaign_id=campaign_id,
            campaign_name=campaign_name
        )
        logging.info(f'Campaign {campaign_id} ({campaign_name}) stopped.')
    return jsonify(response)


@api_campaigns.route('/deleteCampaign', methods=['POST'])
def delete_campaign():

    print('POST api/campaigns/deleteCampaign')

    try:
        request_body = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return 'Failed to get stream.', 404
    else:
        campaign_id = request_body['campaignID']
        campaign_name = request_body['campaignName']

    from TLInterface import get_web_connection
    wc = get_web_connection()

    response = wc.delete_campaign(
        campaign_id=campaign_id,
        campaign_name=campaign_name
    )
    logging.info(f'Campaign {campaign_id} ({campaign_name}) started.')

    return jsonify(response)


@api_campaigns.route('/countCampaignTweets', methods=['POST'])
def count_campaign_tweets():

    try:

        from TLInterface import get_web_connection
        wc = get_web_connection()

        request_body = json.loads(request.data)
        campaign_id = request_body.get('campaignId')
        keywords = request_body.get('keywords')
        start_date = request_body.get('startDate')
        end_date = request_body.get('endDate')
        start_score = request_body.get('startScore')
        end_score = request_body.get('endScore')

        # print()
        # print('Campaign_id:', campaign_id)
        # print('Keywords:', keywords)
        # print('Start date:', start_date)
        # print('End date:', end_date)
        # print('Start score:', start_score)
        # print('End score:', end_score)
        # print()

        data = wc.count_campaign_tweets(campaign_id=campaign_id, key_words=keywords, start_date=start_date, end_date=end_date, start_score=start_score, end_score=end_score)

        if data.get('status') != 200:
            print(data.get('status'))
            print(data.get('msg'))
            return jsonify(False)

        num_tweets = data.get('data', 0)

        return jsonify(num_tweets)

    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return jsonify('Failed to get campaign tweet count.', 404)

    except Exception as e:
        print(e)
        return jsonify('Failed to get campaign tweet count', 404)
