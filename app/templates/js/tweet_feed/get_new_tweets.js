let latestId = 0
let is_streaming = false
let streamLoop
let loadingDots = document.getElementById("loading-dots")

function startLiveStream(interval = 1000) {

    if (!is_streaming) {

        console.log('Starting stream')
        loadingDots.hidden = false
        is_streaming = true

        streamLoop = setInterval(function () {
            getNewTweets()

            if (!is_streaming) {
                clearInterval(streamLoop);
                console.log('Stream closed')
            }
        }, interval);

    } else {
        console.log('Stream is already running.')
    }

}

function stopLiveStream() {
    clearInterval(streamLoop)
    loadingDots.hidden = true
    is_streaming = false
    console.log('Stream stopped')
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
                'nextId': latestId,
                'tweetCutoff': tweetCutoff,
                'numTweets': numTweets,
                'numPages': numPages,
                'ascending': ascending,
                'startScore': startScore,
                'endScore': endScore,
                'keywords': keywords
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

    let newElement = document.createElement('div')
    newElement.classList.add('tweet-container')
    newElement.style.position = "relative"
    newElement.innerHTML = create_tweet_object(tweet, true)
    let loop
    newElement.onclick = function() {
        if (this.getAttribute("name") === "#focus") {
            this.removeAttribute("name")
            clearInterval(loop)
        } else {
            let focusElems = document.getElementsByName("#focus")
            for (let i = 0; i < focusElems.length; i++) {
                focusElems[i].removeAttribute("name")
            }
            this.setAttribute("name", "#focus")
            loop = setInterval(function() {
                let position = document.getElementsByName("#focus")[0].offsetTop - Math.floor(window.innerHeight / 3)
                window.scrollTo(0, position)
            }, 1)
        }
    }
    document.getElementById('tweet-wall').insertBefore(newElement, document.querySelector('#tweet-wall > div'))
}