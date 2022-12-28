function saveTweet(elem) {

    let tweetId = elem.getAttribute('data-tweet')
    let campaignId = elem.getAttribute('data-campaign')

    fetch('{{ url_for("api_feed.save_tweet") }}', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'campaignId': campaignId,
            'tweetId': tweetId
        })
    })
        .then((response) => response.json())
        .then((data) => {
            if (data[1] === 200) {
                elem.classList.add('has-text-success')
                let imgElem = elem.querySelector('span > img')
                imgElem.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/768px-Flat_tick_icon.svg.png"
                imgElem.style.height = "18px"
                imgElem.style.width = "18px"
            }
        })
}
