let latestId = 0
let is_streaming = false

startStream()

function startStream(interval = 1000) {

    console.log('Starting stream')
    is_streaming = true

    let i = setInterval(function(){
        getNewTweets()

        if(!is_streaming) {
            clearInterval(i);
            alert('Stream closed')
        }
    }, interval);

}

function getNewTweets() {

    fetch('{{ url_for("api_feed.get_new_tweets") }}', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'campaignId': campaignId,
                'nextId': latestId
            })
        })
        .then((response) => response.json())
        .then((data) => {
            if (data['status'] === 200) {
                let tweets = data['data']['tweets']
                for (let i = 0; i < tweets.length; i++) {
                    prepend_new_html_object(tweets[i])
                }
                latestId = data['data']['next_id']
            } else {
                console.log(data['status'], '\n', data['message'])
            }
        })
}

function prepend_new_html_object(tweet) {

    console.log(tweet)

    let tweetId = tweet['id']

    let mediaType;
    let mediaUrl;

    try {
        mediaType = tweet['raw']['extended_tweet']['entities']['media'][0]['type']
        mediaUrl = tweet['raw']['extended_tweet']['entities']['media'][0]['media_url']
    } catch (TypeError) {
        mediaType = null
        mediaUrl = null
    }

    let authorProfileImage = tweet['raw']['user']['profile_image_url']
    let authorDisplayName = tweet['raw']['user']['name']
    let authorHandle = tweet['raw']['user']['screen_name']

    let tweetText = tweet['raw']['text']
    try {
        tweetText = tweet['raw']['extended_tweet']['full_text']
    } catch (TypeError) {
    }


    // Tweet hashtags
    let tweetHashtags = tweet['raw']['entities']['hashtags']
    try {
        tweetHashtags = tweet['raw']['extended_tweet']['entities']['hashtags']
    } catch (TypeError) {
    }

    for (let i = 0; i < tweetHashtags.length; i++) {
        let hashtag = tweetHashtags[i]['text']
        tweetText = tweetText.replace(`#${hashtag}`, `<span class="is-electric-blue">#${hashtag}&nbsp;</span>`)
    }


    // User mentions
    let tweetUserMentions = ''
    try {
        tweetUserMentions = tweet['extended_tweet']['entities']['user_mentions']
    } catch (TypeError) {
        try {
            tweetUserMentions = tweet['entities']['user_mentions']
        } catch (TypeError) {
        }
    }

    for (let i = 0; i < tweetUserMentions.length; i++) {
        {#let userId = tweetUserMentions[i]['screen_name']#}
        let userHandle = tweetUserMentions[i]['screen_name']
        {#let userName = tweetUserMentions[i]['name']#}
        tweetText = tweetText.replace(`@${userHandle}`, `<a href="https://twitter.com/${userHandle}" class="is-electric-blue">@${userHandle}</a>`)
    }


    // Tweet links
    let tweetLinks = tweet['raw']['entities']['urls']
    try {
        tweetLinks = tweet['raw']['extended_tweet']['entities']['urls']
    } catch (TypeError) {
    }

    for (let i = 0; i < tweetLinks.length; i++) {
        let displayUrl = tweetLinks[i]['display_url']
        let expandedUrl = tweetLinks[i]['expanded_url']
        let twitterUrl = tweetLinks[i]['url']
        tweetText = tweetText.replace(twitterUrl, `<a href="${expandedUrl}" class="is-electric-blue">${displayUrl}</a>`)
    }


    // Twitter score
    let twitterScore = tweet['twitter_score']


    // HTML Tweet Template
    let html = `
        ${mediaType === 'photo' ? `<img class="tweet-media" src="${mediaUrl}" alt="The image attached to the tweet.">` : ''}

        <div class="tweet-content">

            <div class="columns is-multiline is-vcentered mb-0">

                <a class="tweet-profile-pic column is-narrow pr-1 is-black" href="https://twitter.com/${authorHandle}" target="_blank">
                    <img src="${authorProfileImage}" alt="Profile picture for tweet author.">
                </a>

                <a class="tweet-user-details column is-narrow pl-1 is-black" href="https://twitter.com/${authorHandle}" target="_blank">
                    <div>${authorDisplayName}</div>
                    <div>${authorHandle}</div>
                </a>

                <div class="column is-narrow">
                    <span class="icon-text tweet-track-button">
                        <span class="icon">
                            <img src="{{ url_for('static', filename='images/icons/Plus-Icon.png') }}" alt="Button to track this handle.">
                        </span>
                        <span>TRACK</span>
                    </span>
                </div>

            </div>

            <p class="tweet-text">
                ${tweetText}
            </p>

            <div class="columns mt-1">

                <div class="column">
                    <span class="icon" data-tweet="${tweetId}" data-campaign="${campaignId}" onclick="likeTweet(this);">
                        <i class="far fa-heart"></i>
                    </span>
                </div>

                <div class="tweet-score column has-text-right">
                    <span>TS</span>
                    <span>${twitterScore}</span>
                </div>
            </div>

        </div>

        <hr class="tweet-horizontal-line" />

        <div class="tweet-filter-controls columns is-multiline is-vcentered has-text-left m-1">
            <div class="column is-narrow">
                <span class="icon-text" style="cursor: pointer;" data-tweet="${tweetId}" data-campaign="${campaignId}" onclick="saveTweet(this);">
                    <span class="icon">
                        <img src="{{ url_for('static', filename='images/icons/Plus-Icon.png') }}" alt="">
                    </span>
                    <span>LOCKER</span>
                </span>
            </div>

            <div class="column is-narrow">
                <span class="icon-text" onclick="{# Add a function here that uses fetch to communicate with our api, then flash the response from the api on screen #}">
                    <span class="icon">
                        <img src="{{ url_for('static', filename='images/icons/Plus-Icon.png') }}" alt="">
                    </span>
                    <span>KEYWORDS</span>
                </span>
            </div>

            <div class="column is-narrow">
                <span class="icon-text" onclick="{# Add a function here that uses fetch to communicate with our api, then flash the response from the api on screen #}">
                    <span class="icon">
                        <img src="{{ url_for('static', filename='images/icons/Plus-Icon.png') }}" alt="">
                    </span>
                    <span>HASHTAGS</span>
                </span>
            </div>
        </div>
        {##}
    `

    let newElement = document.createElement('div')
    newElement.classList.add('tweet-container')
    newElement.innerHTML = html
    applyFilters([newElement])
    document.getElementById('tweet-wall').insertBefore(newElement, document.querySelector('#tweet-wall > div'))
}