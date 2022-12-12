import logging

from TLInterface import get_web_connection


def save_new_filter(campaign_id: int, new_filter_name: str, filter_keywords: list[str]) -> list[str] or False:
    try:
        wc = get_web_connection()
        response = wc.save_to_campaign_filters(campaign_id, new_filter_name, filter_keywords)

        print(response.get('msg'))

        if response.get('status') == 200:
            return True
        else:
            return False

    except Exception as e:
        logging.error(e)
        return False


def get_filters(campaign_id: int) -> list[dict] or False:
    try:
        wc = get_web_connection()
        response = wc.get_campaign_filters(campaign_id)

        print('\n' + response.get('msg') + '\n')

        if response.get('status') == 200:
            return response.get('data')
        else:
            return False

    except Exception as e:
        logging.error(e)
        return False


if __name__ == '__main__':
    # save_new_filter(60, 'test filter', ['test', 'christmas'])
    print(get_filters(60))
    pass
