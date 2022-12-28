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
        start_score = request_body.get('startScore')
        end_score = request_body.get('endScore')
        start_date = request_body.get('startDate')
        end_date = request_body.get('endDate')

        from datetime import datetime

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            start_date = start_date.strftime('%d-%m-%Y')
        else:
            start_date = None

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = end_date.strftime('%d-%m-%Y')
        else:
            end_date = None

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
            # print(data.get('status'))
            # print(data.get('msg'))
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


@api_campaigns.route('/getCampaignFilters', methods=['POST'])
def get_campaign_filters():

    print('\ncalled /getCampaignFilters!\n')

    try:
        request_body = json.loads(request.data)
        campaign_id = request_body.get('campaignId')

        from TLInterface.filter_sets import get_filters
        response = get_filters(campaign_id)

        if response:
            return jsonify({
                'status': 200,
                'message': "Success",
                'data': response
            })
        else:
            return jsonify({
                'status': 400,
                'message': "Failed to get campaign filters. See server logs.",
                'data': None
            })

    except Exception as e:
        print(e)
        return jsonify({
            'status': 400,
            'message': "Unknown error. See server logs.",
            'data': None
        })


@api_campaigns.route('/saveCampaignFilter', methods=['POST'])
def save_campaign_filter():

    print('called /saveCampaignFilter!')

    try:
        request_body = json.loads(request.data)
        campaign_id = request_body.get('campaignId')
        filter_name = request_body.get('filterName')
        filter_keywords = request_body.get('filterKeywords')

        from TLInterface.filter_sets import save_new_filter
        response = save_new_filter(campaign_id, filter_name, filter_keywords)

        if response:
            return jsonify({
                'status': 200,
                'message': "Success",
                'data': None
            })
        else:
            return jsonify({
                'status': 400,
                'message': "Failed to get campaign filters. See server logs.",
                'data': None
            })

    except Exception as e:
        print(e)
        return jsonify({
            'status': 400,
            'message': "Unknown error. See server logs.",
            'data': None
        })


@api_campaigns.route('/deleteCampaignFilter', methods=['POST'])
def delete_campaign_filter_set():

    try:
        print('api/Campaigns/deleteCampaignFilter called!')

        from TLInterface import get_web_connection
        wc = get_web_connection()

        request_body = json.loads(request.data)
        campaign_id = request_body.get('campaignId')
        filter_name = request_body.get('filterName')

        response = wc.delete_from_campaign_filters(
                        campaign_id=campaign_id,
                        filter_name=filter_name)

        print(response)
        return jsonify(True if response.get('status') == 200 else False)

    except Exception as e:
        logging.error(e)
        return jsonify(False)

@api_campaigns.route('/addCampaignKeywords', methods=['POST'])
def add_campaign_keywords():

    try:

        success = True

        request_body = json.loads(request.data)
        campaign_id = request_body.get('campaignId')
        keywords = request_body.get('keywords')

        from TLInterface import get_web_connection

        wc = get_web_connection()

        for pos_key in keywords['positive']:
            print(f"Storing positive keyword:  {pos_key}")
            response = wc.store_campaign_keyword(
                campaign_id=campaign_id,
                keyword_type='positive',
                keyword_text=pos_key,
            )
            print(response)
            if response.get('status') != 200:
                success = False

        for neg_key in keywords['negative']:
            print(f"Storing negative keyword:  {neg_key}")
            response = wc.store_campaign_keyword(
                campaign_id=campaign_id,
                keyword_type='negative',
                keyword_text=neg_key,
            )
            print(response)
            if response.get('status') != 200:
                success = False

        return jsonify(success)

    except Exception as e:
        logging.error(e)
        return jsonify(
            False
        )

