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

let campaignTweetCountOriginal = document.getElementById("campaign-tweet-count")
let campaignTweetCountClone = document.getElementById("campaign-tweet-count-locker")


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

    campaignTweetCountOriginal.hidden = false
    campaignTweetCountClone.hidden = true

    try {
        checkForNewTweets()
    }
    catch (ReferenceError) {
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
            if (lockerTweets) {

                keywords = []
                setupPage(keywords)

                let lockerLength = lockerTweets.length

                for (let i = 0; i < lockerLength; i++) {
                    append_new_html_object(lockerTweets[i])
                }

                for (let i = 0; i < excludedTweets.length; i++) {
                    if (tweetLocker.includes(excludedTweets[i])) {
                        lockerLength -= 1
                    }
                }

                campaignTweetCountClone.innerHTML = "— " + lockerLength + " tweets"
                campaignTweetCountClone.hidden = false
                campaignTweetCountOriginal.hidden = true
            } else {
                alert('No tweets saved to locker yet!')
            }
        })
}



function loadHiddenTweetsFunc() {
    fetch(`{{ url_for('api_campaigns.get_excluded_tweets') }}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'campaignId': campaignId
            })
        })
        .then((response) => response.json())
        .then((hiddenTweets) => {
            if (hiddenTweets) {

                keywords = []
                setupPage(keywords)

                for (let i = 0; i < hiddenTweets.length; i++) {
                    append_new_html_object(hiddenTweets[i], true)
                }

                campaignTweetCountClone.innerHTML = "— " + hiddenTweets.length + " tweets"
                campaignTweetCountClone.hidden = false
                campaignTweetCountOriginal.hidden = true
            } else {
                alert("You haven't hidden any tweets yet!")
            }
        })
}


function applyFilters(tweetElems = undefined, mode = 'old', keywords = undefined, loadTweetLocker = false, loadHiddenTweets = false) {
    /* This function applies current page filters to all tweets or just the ones specified by tweetElems argument */

    let tweetWall = document.getElementById('tweet-wall')
    tweetWall.replaceChildren()

    if (loadTweetLocker) {
        loadTweetLockerFunc()
    } else if (loadHiddenTweets) {
        loadHiddenTweetsFunc()
    } else {

        setupPage(keywords)

        if (mode === 'old' || mode === undefined) {
            getOldTweets()
        }

    }

}
