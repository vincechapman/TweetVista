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

function retweet(elem, tweetId) {

    let retweetMode

    // if (elem.childNodes[1].classList.contains('has-text-success')) {
    //     elem.childNodes[1].classList.remove('has-text-success')
    //     retweetMode = 'delete'
    // } else {
    //     elem.childNodes[1].classList.add('has-text-success')
    //     retweetMode = 'retweet'
    // }

    elem.childNodes[1].classList.add('has-text-success')

    fetch("{{ url_for('api_feed.retweet') }}", {
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
            if (!success) {
                alert(`Failed to retweet. Please try again later or contact us if the issue persists.`)
                elem.childNodes[1].classList.remove('has-text-success')
            }
        })

}

function reply(elem, tweetId, handle) {

    let container = elem.parentElement.parentElement.parentElement

    let thisReplyBox = container.querySelector("#reply-text-box")

    if (thisReplyBox) {
        thisReplyBox.parentElement.remove()
        elem.classList.remove('is-bright-orange')

    } else {
        // Removes any reply boxes that were previously opened
        let oldReplyBox = document.querySelector("#reply-text-box")
        if (oldReplyBox) {
            oldReplyBox.parentElement.remove()
        }

        // Creates a new reply box
        let newElem = document.createElement('div')
        newElem.style.position = "relative"
        newElem.innerHTML = `
            <textarea id='reply-text-box' class='input has-text-grey' maxlength="280" oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'></textarea>
            <button class="button is-link is-small is-rounded" style="position: absolute; bottom: 10px; right: 10px" onclick="sendReply(this, '${tweetId}', '${handle}')">
                <span class="icon">
                    <i class="fas fa-paper-plane"></i>
                </span>
                <span>Send reply</span>
            </button>`
        container.appendChild(newElem)
        newElem.firstElementChild.focus()

        elem.classList.add('is-bright-orange')
    }

    // alert("No support for replies yet.")
}

function sendReply(elem, tweetId, handle) {
    let replyText = elem.previousElementSibling.value
    let quoteTweet = false
    let image = undefined
    let name = ""
    let url =  undefined
    let shortUrl = ""

    fetch("{{ url_for('api_feed.reply_to_tweet') }}", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'campaignId': campaignId,
            'replyText': replyText,
            'tweetId': tweetId,
            'handle': handle,
            'quoteTweet': quoteTweet,
            'image': image,
            'name': name,
            'url': url,
            'shortUrl': shortUrl
        })
    })
        .then((response) => response.json())
        .then((success) => {
            if (!success) {
                alert(`Failed to reply to tweet. Please try again later or contact us if the issue persists.`)
            }
            elem.parentElement.previousElementSibling.lastElementChild.previousElementSibling.firstElementChild.classList.remove('is-bright-orange')
            elem.parentElement.remove()
        })
}
