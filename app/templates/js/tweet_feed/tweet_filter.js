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

let lowestTweetScore = 0

let startDate = undefined
let endDate = undefined

let positiveKeywords;  // Only return tweets that contain this keyword.
let negativeKeywords; // Only return tweets that do not contain this keyword.


let tweets
let nextPage
// let keywords
let tweetCutoff
// let startDate
// let endDate
let numTweets
let numPages
let ascending
let fetchedPages = []  // A temporary measure to stop multiple requests for one page of old tweets


function setupPage() {
    nextPage = 1
    tweetCutoff = undefined

    keywords = document.getElementById('new-search-words').value

    // startDate = undefined  // TODO Change to get value from date input. The minimum and maximum dates should be set to campaign start and today's date respectively
    // endDate = undefined  // TODO Change to get value from date input. The minimum and maximum dates should be set to campaign start and today's date respectively

    startScore = parseInt(document.getElementById('tweet-score-limit').value)
    endScore = undefined

    numTweets = undefined
    numPages = undefined

    ascending = false  // TODO Change to get value from a dropdown

    fetchedPages = []

    let tweetCountContainer = document.getElementById('new-tweet-count-container')
    if (tweetCountContainer) {
        tweetCountContainer.classList.add('is-hidden')
    }
}




function applyFilters(tweetElems = undefined, mode = 'old') {
    /* This function applies current page filters to all tweets or just the ones specified by tweetElems argument */

    let tweetWall = document.getElementById('tweet-wall')
    tweetWall.replaceChildren()

    setupPage()

    if (mode === 'old') {
        getOldTweets()
    }

}

function tweetScoreRule(elem, lowestTweetScore) {
    // Checks if current tweet satisfies minimum tweet score rule, if not returns False.
    if (lowestTweetScore > 0) {
        let tweetScore = parseInt(elem.querySelector('div.tweet-content > div.columns > div.tweet-score > span:nth-child(2)').innerText)
        return tweetScore >= lowestTweetScore
    } else {
        return true
    }
}

function keywordsRule(elem) {
    return true
}

function dateRangeRule(elem) {
    return true
}