let latestTweetCount;

let checkForNewTweetsLoop = setInterval(checkForNewTweets, 5000)

function checkForNewTweets() {
    fetch('{{ url_for("api_campaigns.count_campaign_tweets") }}', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'campaignId': campaignId,
                'keywords': keywords,
                'startDate': startDate,
                'endDate': endDate,
                'startScore': startScore,
                'endScore': endScore,
            })
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            latestTweetCount = data
            if (latestTweetCount !== numTweets) {
                console.log(latestTweetCount - numTweets, 'new tweets')
                let newTweetCountElem = document.getElementById('new-tweet-count')
                let numNewTweets = latestTweetCount - numTweets
                newTweetCountElem.innerHTML = `<span class="has-text-weight-bold">${numNewTweets}</span> new tweet${numNewTweets === 1 ? '' : 's'}`

                let tweetCountContainer = newTweetCountElem.parentNode.parentNode
                tweetCountContainer.classList.remove('is-hidden')
            }
        })
}