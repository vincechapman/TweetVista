to authorise a users twitter account

the oauth functions are in oauth.py in the package AccessTLIServer
the api functions 

    get_current_twitter_app()
    store_user_twitter_credentials(only_tokens)

have not been written yet
I still need to test this fully

1) get the app keys using tlapi 

   keys = get_current_twitter_app()

2) construct the twitter callback 

    callback = construct_twitter_callback()
 
3) get the oauth request tokens
    
   
        ck = keys['consumer_key']
        cs = keys['consumer_secret']
        ro_key,ro_secret = twitter_get_oauth_request_token(cs,ck,callback) 
  save twitter_app data in session

        twitter_app={'app_name':app.name,'consumer_key':ck,'consumer_secret':cs,'resource_owner_key':ro_key,'resource_owner_secret':ro_secret}
4) get twitter to authorise account
   use request to go to twitter

   url = 'https://api.twitter.com/oauth/authorize?oauth_token='+ro_key+'&force_login=true' 
  redirect to url

5) handle the call back 
   http://127.0.0.1:8000/twitter/login/callback
   
   retrieve twitter_app from session,
   get oauth_token from the request
   get oauth_verifier from the request

        access_token_list=twitter_get_oauth_token(oauth_verifier,twitter_app)
        access_tokens=twitter_get_access_tokens(access_token_list,twitter_app)
        only_tokens = {i:access_tokens[i] for i in access_tokens}
        only_tokens['user_data'] = verify_twitter_credentials(access_tokens)
        only_tokens['app_name'] = request.session.pop('twitter_appname', None)

    call api to store user twitter keys
 
    store_user_twitter_credentials(only_tokens)
