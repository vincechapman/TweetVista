import logging

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

campaigns = Blueprint('campaigns', __name__, url_prefix='/campaigns')


@campaigns.route('/', methods=['GET', 'POST'])
def main():

    if request.method == 'POST':

        if request.form['submit'] == 'create-campaign':

            from TLInterface.get_campaigns import get_web_connection
            wc = get_web_connection()

            form_data = request.form.to_dict()

            # ----------------------------------------------------------------
            # Creating a new campaign

            if form_data['campaign-type'] != 'affiliate':
                form_data['affiliate-name'] = None
                form_data['affiliate-url'] = None
                form_data['affiliate-short-url'] = None

            response = wc.create_client_campaign(
                campaign_name=form_data['campaign-name'],
                campaign_type=form_data['campaign-type'],
                affiliate_name=form_data['affiliate-name'],
                affiliate_url=form_data['affiliate-url'],
                affiliate_short=form_data['affiliate-short-url']
            )

            print('Create client campaign response: ', response)

            # ----------------------------------------------------------------
            # Adding keywords for new campaign

            if response['status'] == 200 and (form_data['campaign-type'] != 'profile'):

                new_campaign_id = response['data']['campaign_id']

                keywords = {
                    'positive': {},
                    'negative': {}
                }

                for field in form_data:

                    if field.startswith('positive-keywords-field') or field.startswith('negative-keywords-field'):
                        data = field.split('|')
                        row_number = data[1]
                        data_type = data[2]
                        value = form_data[field]

                        if field.startswith('positive-keywords-field'):
                            try:
                                keywords['positive'][row_number]
                            except KeyError:
                                keywords['positive'][row_number] = {}
                            finally:
                                keywords['positive'][row_number][data_type] = value

                        elif field.startswith('negative-keywords-field'):
                            try:
                                keywords['negative'][row_number]
                            except KeyError:
                                keywords['negative'][row_number] = {}
                            finally:
                                keywords['negative'][row_number][data_type] = value

                from pprint import pprint
                pprint(keywords, indent=4)

                for kw_set in keywords:
                    for kw in keywords[kw_set]:
                        keyword = keywords[kw_set][kw]['keyword']
                        kw_type = keywords[kw_set][kw]['type']
                        if kw_type == 'Exact Order':
                            order = 'fixed'
                        elif kw_type == 'Any Order':
                            order = 'any'
                        else:
                            logging.warning('There is no order for this on the backend, so have just set as "any"')
                            order = 'any'
                        response = wc.store_campaign_keyword(
                            campaign_id=new_campaign_id,
                            keyword_text=keyword,
                            keyword_type=kw_set,
                            keyword_order=order,
                        )
                        print('Store positive keyword - response:', response)

                response = wc.start_campaign_feed(new_campaign_id)
                print('Start campaign - response:', response)

    from TLInterface.get_campaigns import get_all_campaigns
    all_campaigns = get_all_campaigns()

    from helpers.countries import get_countries
    countries_list = get_countries()

    return render_template('pages/campaigns/main.html', campaigns=all_campaigns, countries_list=countries_list)


@campaigns.route('/<int:campaign_id>', methods=['GET', 'POST'])
def view_campaign(campaign_id):

    from TLInterface.get_campaigns import get_all_campaigns, get_campaign_data

    # Basic data for all campaigns
    all_campaigns = get_all_campaigns()

    # Data for this campaign
    campaign_data = get_campaign_data(campaign_id)
    campaign_is_active = campaign_data['is_active'] if campaign_data else False

    is_live = False

    if request.method == 'POST':
        submit_button = request.form.get('submit')
        if submit_button:
            if submit_button == 'make-live':
                is_live = True
            elif submit_button == 'make-not-live':
                is_live = False
            elif submit_button == 'reactivate-campaign':
                print('Reactivating campaign!')

                from TLInterface import get_web_connection
                wc = get_web_connection()

                response = wc.start_campaign_feed(
                    campaign_id=campaign_id)

                if response.get('status'):
                    logging.info(f'Campaign {campaign_id} started.')
                    campaign_is_active = True

                is_live = True

            else:
                print('Invalid live button value')
        else:
            selected_campaign = request.form['campaign-selection']
            print('SELECTED CAMPAIGN:', selected_campaign)
            return redirect(url_for('campaigns.view_campaign', campaign_id=selected_campaign))

    return render_template('pages/campaigns/view_campaign.html', all_campaigns=all_campaigns, selected_campaign=campaign_id, is_live=is_live, campaign_is_active=campaign_is_active)
