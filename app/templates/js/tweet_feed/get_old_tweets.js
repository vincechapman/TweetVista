/*
TODO Some profile images aren't loading properly - the link is not working. But when you click to their profile, there is an image. So look into how we can solve this.
 Even if we just use a default image in the meantime.

TODO Look into combining the html tweet objects for the getOldTweets and getNewTweets function so we don't have to manage two different versions of this.
*/

// setupPage()

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

function append_new_html_object(tweet, showExcluded = false) {
    let newElement = document.createElement('div')
    newElement.classList.add('tweet-container')
    newElement.style.position = "relative"
    newElement.innerHTML = create_tweet_object(tweet, false, showExcluded)
    document.getElementById('tweet-wall').appendChild(newElement)
}
