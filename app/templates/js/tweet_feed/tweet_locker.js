function callApi(endpoint, method, body) {
    fetch(endpoint, {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
        .then((response) => {
            return response.json()
        })
    return false;  // If this runs, then fetch failed.
}

function saveTweet(elem) {

    let tweetId = elem.getAttribute('data-tweet')
    let campaignId = elem.getAttribute('data-campaign')

    let response = callApi(
        '{{ url_for("api_feed.save_tweet") }}',
        'POST',
        {
            'campaignId': campaignId,
            'tweetId': tweetId
        }
    )
    alert(response)
}
