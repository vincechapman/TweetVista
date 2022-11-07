function callApi(endpoint, method, body) {
    return fetch(endpoint, {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
        .then((response) => {
            return response.json().then((data) => {
                console.log(data)
                return data
            })
        })
    // return false;  // If this runs, then fetch failed.
}

function saveTweet(elem) {

    let tweetId = elem.getAttribute('data-tweet')
    let campaignId = elem.getAttribute('data-campaign')

    callApi(
        '{{ url_for("api_feed.save_tweet") }}',
        'POST',
        {
            'campaignId': campaignId,
            'tweetId': tweetId
        }
    )
        .then((response) => {
            response.json().then((data) => {
                console.log(data)
                alert(data)
            })
        })
}
