function saveTweetToLocker(elem) {

    let tweetId = elem.getAttribute('data-tweet')
    let campaignId = elem.getAttribute('data-campaign')

    fetch('{{ url_for("api_feed.save_tweet_to_locker") }}', {
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
                tweetLocker.push(String(tweetId))
            }
        })
}

function deleteTweetFromLocker(elem) {

    let tweetId = elem.getAttribute('data-tweet')
    let campaignId = elem.getAttribute('data-campaign')

    fetch('{{ url_for("api_feed.delete_tweet_from_locker") }}', {
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
        .then((success) => {
            if (success) {
                elem.lastElementChild.classList.remove('has-text-success')
                let imgElem = elem.querySelector('span > img')
                imgElem.src = "{{ url_for('static', filename='images/icons/Plus-Icon.png') }}"
                imgElem.style.height = "initial"
                imgElem.style.width = "initial"
                tweetLocker.splice(tweetLocker.indexOf(String(tweetId)), 1)
            }
        })
}