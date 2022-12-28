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

let keywords = []
let keywordInput = document.getElementById('new-search-words')

let startDate = undefined
let endDate = undefined

let startDateElem = document.getElementById('start-date')
let endDateElem = document.getElementById('end-date')

let startScore, endScore
let tweetCutoff
let numTweets
let numPages
let ascending

let liveMode = false
let viewBusinesses, viewPrivateUsers = true


Array.prototype.unique = function() {
    let a = this.concat();
    for(let i=0; i<a.length; ++i) {
        for(let j=i+1; j<a.length; ++j) {
            if(a[i] === a[j])
                a.splice(j--, 1);
        }
    }

    return a;
};


function setupPage(setKeywords) {
    // This function sets/resets appropriate variables every time filter is applied

    nextPage = 1
    tweetCutoff = undefined
    numTweets = undefined
    numPages = undefined
    ascending = false  // TODO Change to get value from a dropdown

    startDate = startDateElem.value
    endDate = endDateElem.value

    if (startDate) {
        endDateElem.setAttribute("min", startDate)
    } else {
        endDateElem.removeAttribute("min")
    }

    if (endDate) {
        startDateElem.setAttribute("max", endDate)
    } else {
        startDateElem.removeAttribute("max")
    }

    // Setting up keywords variable
    if (setKeywords === undefined) {
        let currentInput = keywordInput.value.split(",")
        for (let i = 0; i < currentInput.length; i++) {
            if (currentInput[i] === "") {
                currentInput.splice(i, 1)
            }
        }
        keywords = keywords.concat(currentInput).unique();  // Merges old keyword list with new keyword list and removes duplicates
        for (let i = 0; i < keywords.length; i++) {
            keywords[i] = keywords[i].trim()
        }
        if (keywords.length === 1 && keywords[0] === "") {
            keywords = []
        }
    }
    // else {
    //     k
    // }

    keywordInput.value = ""  // Clears input field

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
            keywords = []
            setupPage(keywords)
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
