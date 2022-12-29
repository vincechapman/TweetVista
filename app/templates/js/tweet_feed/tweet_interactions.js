function likeTweet(elem) {

    let mode = ''

    if (elem.childNodes[1].classList.contains('far')) {
        elem.childNodes[1].classList.remove('far')
        elem.childNodes[1].classList.add('fas', 'is-hot-pink')
        mode = 'like'
    } else if (elem.childNodes[1].classList.contains('fas')) {
        elem.childNodes[1].classList.remove('fas', 'is-hot-pink')
        elem.childNodes[1].classList.add('far')
        mode = 'unlike'
    }

    fetch("{{ url_for('api_feed.like_tweet') }}", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'campaign': elem.getAttribute('data-campaign'),
            'tweet': elem.getAttribute('data-tweet'),
            'like_or_unlike': mode
        })
    })
        .then((response) => response.json())
        .then((success) => {
            if (!success) {
                alert(`Failed to ${mode} this tweet. Please try again later or contact us if the issue persists.`)
                if (mode === "unlike") {
                    elem.childNodes[1].classList.remove('far')
                    elem.childNodes[1].classList.add('fas', 'is-hot-pink')
                } else {
                    elem.childNodes[1].classList.remove('fas', 'is-hot-pink')
                    elem.childNodes[1].classList.add('far')
                }
            }
        })
}

function followUser(elem) {
    // Handles the following (and unfollowing) of Twitter accounts

    let mode

    if (elem.childNodes[1].classList.contains('far')) {
        elem.childNodes[1].classList.remove('far')
        elem.childNodes[1].classList.add('fas', 'has-text-info')
        mode = 'follow'
    } else if (elem.childNodes[1].classList.contains('fas')) {
        elem.childNodes[1].classList.remove('fas', 'has-text-info')
        elem.childNodes[1].classList.add('far')
        mode = 'unfollow'
    }

    fetch("{{ url_for('api_feed.follow_user') }}", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'campaign': elem.getAttribute('data-campaign'),
            'handle': elem.getAttribute('data-handle'),
            'mode': mode
        })
    })
        .then((response) => response.json())
        .then((success) => {
            if (!success) {
                alert(`Failed to ${mode} this account. Please try again later or contact us if the issue persists.`)
                if (mode === 'unfollow') {
                    elem.childNodes[1].classList.remove('far')
                    elem.childNodes[1].classList.add('fas', 'has-text-info')
                } else {
                    elem.childNodes[1].classList.remove('fas', 'has-text-info')
                    elem.childNodes[1].classList.add('far')
                }
            }
        })
}

function retweet(elem) {
    // Handles the following (and unfollowing) of Twitter accounts

    let retweetMode

    if (elem.childNodes[1].classList.contains('has-text-success')) {
        elem.childNodes[1].classList.remove('has-text-success')
        retweetMode = 'delete'
    } else {
        elem.childNodes[1].classList.add('has-text-success')
        retweetMode = 'retweet'
    }

    alert("No support for retweet yet.")

}

