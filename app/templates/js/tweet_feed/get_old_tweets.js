/*
TODO Some profile images aren't loading properly - the link is not working. But when you click to their profile, there is an image. So look into how we can solve this.
 Even if we just use a default image in the meantime.

TODO Look into combining the html tweet objects for the getOldTweets and getNewTweets function so we don't have to manage two different versions of this.
*/

setupPage()
getOldTweets()

function getOldTweets() {
    let tweetWall = document.getElementById('tweet-wall')

    tweets = undefined

    fetch('{{ url_for("api_feed.get_old_tweets") }}', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'campaignId': campaignId,
                'nextPage': nextPage,
                'tweetCutoff': tweetCutoff,
                'numTweets': numTweets,
                'numPages': numPages,
                'ascending': ascending,
                'startScore': startScore,
                'endScore': endScore,
                'startDate': startDate,
                'endDate': endDate,
                'keywords': keywords
            })
        })
        .then((response) => response.json())
        .then((data) => {
            if (data['status'] === 200) {

                tweets = data['data']['tweets']
                nextPage = data['data']['nextPage']
                numPages = data['data']['numPages']  // TODO Use numPages here to set up pagination
                numTweets = data['data']['numTweets']
                tweetCutoff = data['data']['tweetCutoff']

                setupPages(numPages, nextPage - 1)

                tweetWall.replaceChildren()

                for (let i = 0; i < tweets.length; i++) {
                    append_new_html_object(tweets[i])
                }

            }

        })
}

function append_new_html_object(tweet) {

    let tweetId = tweet['id']

    if (excludedTweets.includes(String(tweetId))) {
        return;
    }

    let savedInLocker = tweetLocker.includes(String(tweetId))

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

    let tweetDate = tweet['created_at']

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
        tweetHashtags[i] = '#' + tweetHashtags[i]['text']
        tweetText = tweetText.replace(`${tweetHashtags[i]}`, `<span class="is-electric-blue">${tweetHashtags[i]}&nbsp;</span>`)
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
        let userHandle = tweetUserMentions[i]['screen_name']
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

        <div class="tweet-content-overlay"></div>

        ${mediaType === 'photo' ? `
            <img class="tweet-media" src="${mediaUrl}" alt="The image attached to the tweet."
            onclick="">
            ` : ''}

        <div class="tweet-content">
        
            <div class="columns is-multiline is-vcentered mb-0">

                <a class="tweet-profile-pic column is-narrow pr-1 is-black" href="https://twitter.com/${authorHandle}" target="_blank">
                    <img src="${authorProfileImage}" alt="Profile picture for tweet author.">
                </a>

                <a class="tweet-user-details column pl-1 is-black" href="https://twitter.com/${authorHandle}" target="_blank" style="overflow: hidden; white-space: nowrap; position: relative;">
                    <div>${authorDisplayName}</div>
                    <div>${authorHandle}</div>
                    <div style="position: absolute; height: 100%; width: 100%; background: linear-gradient(90deg, rgba(0,0,0,0) 95%, white); top: 0; left: 0"></div>
                </a>

                <div class="column is-narrow">
                        <div class="dropdown is-right"
                        onmouseover="this.closest('.tweet-container').firstElementChild.classList.add('visible'); this.classList.add('is-active')"
                        onmouseleave="this.closest('.tweet-container').firstElementChild.classList.remove('visible'); this.classList.remove('is-active')">
                            <div class="dropdown-trigger">
                                <span class="icon is-clickable">
                                    <i class="fas fa-ellipsis-v has-text-grey-light"></i>
                                </span>
                            </div>
                            <div class="dropdown-menu" id="dropdown-menu2" role="menu">
                                <div class="dropdown-content">
                                    <div class="dropdown-item">
                                        <span class="icon-text">
                                            <span class="icon">
                                                <i class="fas fa-binoculars is-electric-blue"></i>
                                            </span>
                                            <span>Track user's posts</span>
                                        </span>
                                    </div>
                                    <div class="dropdown-item"  onclick="excludeTweets(this, ${tweetId})">
                                        <span class="icon-text">
                                            <span class="icon">
                                                <i class="fas fa-times-circle has-text-danger"></i>
                                            </span>
                                            <span>Exclude tweet</span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                </div>



            </div>
            
            <p class="is-size-7 mb-3 has-text-grey-light">${tweetDate}</p>

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
                    <span>TweetScore</span>
                    <span>${twitterScore}</span>
                </div>
            </div>

        </div>

        <hr class="tweet-horizontal-line" />

        <div class="tweet-filter-controls columns is-multiline is-vcentered has-text-left m-1">
            <div class="column is-narrow">
                <span class="icon-text" style="cursor: pointer;" data-tweet="${tweetId}" data-campaign="${campaignId}" onclick="${savedInLocker ? `deleteTweetFromLocker(this)` : `saveTweetToLocker(this)`}">
                    <span class="icon">
                        ${savedInLocker ? `<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/768px-Flat_tick_icon.svg.png" style="height: 18px; width: 18px;">`
                                        : `<img src="{{ url_for('static', filename='images/icons/Plus-Icon.png') }}">`}
                    </span>
                    <span class="${savedInLocker ? `has-text-success` : ``}">LOCKER</span>
                </span>
            </div>

            <div class="column is-narrow">
                <span class="icon-text is-clickable" onclick="createKeywordPopup(this, '${tweet['word_tokens']}', 'keywords')">
                    <span class="icon">
                        <img src="{{ url_for('static', filename='images/icons/Plus-Icon.png') }}" alt="">
                    </span>
                    <span>KEYWORDS</span>
                </span>
            </div>

            <div class="column is-narrow">
                <span class="icon-text is-clickable" onclick="createKeywordPopup(this, '${tweetHashtags}', 'hashtags')">
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
    newElement.style.position = "relative"
    newElement.innerHTML = html
    document.getElementById('tweet-wall').appendChild(newElement)
}
