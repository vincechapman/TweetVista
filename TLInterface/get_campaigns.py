import logging
from pprint import pprint
from TLInterface import get_web_connection


def get_all_campaigns() -> list:

    """Returns a list of all campaigns"""

    wc = get_web_connection()
    campaigns = []

    try:
        all_campaigns = wc.get_client_campaigns()
    except Exception as e:
        logging.error(f'Failed to get client campaigns, due to following error:\n\n{e}')
    else:
        campaigns = all_campaigns.get('data', [])

    return campaigns


def get_campaign_data(campaign_id: int) -> dict:

    """Returns details for the specified campaign. If no campaign_id is provided, the first available campaign is returned"""

    wc = get_web_connection()
    if wc is False:
        return {}  # Returns empty dictionary if no web connection

    try:
        ret_dict = wc.get_client_campaign_by_id(campaign_id)
    except Exception as e:
        logging.error(f'Failed to get campaign data from TLApi:\n{e}')
        return {}

    campaign_data = ret_dict.get('data', {})

    if not campaign_data:
        logging.error(f'No data found for campaign with id: {campaign_id}')

    return campaign_data


def get_first_campaign_id() -> int:

    all_campaigns = get_all_campaigns()

    if all_campaigns:
        first_campaign = all_campaigns[0]
        first_campaign_id = first_campaign.get('id', '0')
        return first_campaign_id
    else:
        return False
