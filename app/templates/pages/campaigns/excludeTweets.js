function excludeTweets(elem, tweetId) {
    fetch("{{ url_for('api_campaigns.exclude_tweets') }}", {
        method: "POST",
        body: JSON.stringify({
                'campaignId': campaignId,
                'tweetId': tweetId
            })
    })
        .then((response) => response.json())
        .then((success) => {
            if (success) {
                console.log("Tweet successfully excluded from showing up again.")
                elem.closest('.tweet-container').remove()
                excludedTweets.push(String(tweetId))
            } else {
                alert("Failed to exclude tweet. Please try again later or contact us.")
            }
        })
}