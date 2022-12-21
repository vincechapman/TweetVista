/*
REQUIREMENTS

This filter needs two modes
- Filter all tweets that have been loaded so far
- Filter new tweets that are being added

Ideally this one filter should cover all filtering needs i.e.
- Date range filtering
- TweetScore filtering
- Keyword & Hashtag filters
(And any combination of these)
*/

let tweets
let nextPage
let keywords
let startDate = undefined
let endDate = undefined
let startScore, endScore
let tweetCutoff
let numTweets
let numPages
let ascending


function setupPage(setKeywords) {
    // This function sets/resets appropriate variables every time filter is applied

    nextPage = 1
    tweetCutoff = undefined
    numTweets = undefined
    numPages = undefined
    ascending = false  // TODO Change to get value from a dropdown

    // Setting up keywords variable
    if (setKeywords === undefined) {
        keywords = document.getElementById('new-search-words').value.split(",")
        for (let i = 0; i < keywords.length; i++) {
            keywords[i] = keywords[i].trim()
        }
        if (keywords.length === 1 && keywords[0] === "") {
            keywords = []
        }
    } else {
        document.getElementById('new-search-words').value = setKeywords.join(", ")
    }

    // Other filter variables
    startScore = parseInt(document.getElementById('tweet-score-limit').value)
    endScore = 700
    // startDate = undefined  // TODO Change to get value from date input. The minimum and maximum dates should be set to campaign start and today's date respectively
    // endDate = undefined  // TODO Change to get value from date input. The minimum and maximum dates should be set to campaign start and today's date respectively


    let tweetCountContainer = document.getElementById('new-tweet-count-container')
    if (tweetCountContainer) {
        tweetCountContainer.classList.add('is-hidden')
    }

    setupFilterSummary()

}


function loadTweetLockerFunc() {
    fetch('/locker/' + campaignId, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        .then((response) => response.json())
        .then((lockerTweets) => {
            console.log('Saved tweets!')
            console.log(lockerTweets)
            if (lockerTweets) {
                    for (let i = 0; i < lockerTweets.length; i++) {
                        append_new_html_object(lockerTweets[i])
                    }
            } else {
                alert('No tweets saved to locker yet!')
            }
        })
}


function applyFilters(tweetElems = undefined, mode = 'old', keywords = undefined, loadTweetLocker = false) {
    /* This function applies current page filters to all tweets or just the ones specified by tweetElems argument */

    let tweetWall = document.getElementById('tweet-wall')
    tweetWall.replaceChildren()

    if (loadTweetLocker) {
        loadTweetLockerFunc()
    } else {

        setupPage(keywords)

        if (mode === 'old' || mode === undefined) {
            getOldTweets()
        }

    }

}
