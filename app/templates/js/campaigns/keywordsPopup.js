let parent = document.getElementById('keyword-modal')

function createKeywordPopup(elem, tokens) {

    let keywordPopups = document.getElementsByClassName('keywords-popup')
    for (let i = 0; i < keywordPopups.length; i++) {
        keywordPopups[i].remove()
    }

    tokens = tokens.split(',')

    let htmlTokens = ''

    let alignmentOptions = ['has-text-left', 'has-text-centered', 'has-text-right']
    let alignmentOptionsIndex = 0

    for (let i = 0; i < tokens.length; i++) {
        htmlTokens += `
            <div class="column is-one-third ${alignmentOptions[alignmentOptionsIndex]}">
                <span>
                    <span>${tokens[i]}</span>
                    <span>
                        <i class="fas fa-plus-circle is-electric-blue is-clickable" onclick="selectPositiveKeyword(this)"></i>
                        <i class="fas fa-minus-circle has-text-danger is-clickable" onclick="selectNegativeKeyword(this)"></i>
                    </span>
                </span>
            </div>
        `
        alignmentOptionsIndex === 2 ? alignmentOptionsIndex = 0 : alignmentOptionsIndex++
    }

    let newElem = document.createElement('div')

    newElem.style.maxWidth = '600px'
    newElem.style.position = 'relative'
    newElem.classList.add('border-is-electric-blue', 'keywords-popup', 'is-unselectable', 'modal-content', 'bg-is-white')

    newElem.innerHTML = `

    <span class="icon" style="position: absolute; top: 5px; right: 5px">
        <i class="fas fa-times-circle is-electric-blue is-clickable" onclick="closeWindow(this)"></i>
    </span>

    <div class="p-4">

        <p><span class="is-electric-blue">Add</span> Keywords to your Campaign</p>
        <div class="columns is-variable is-1 mt-1">
            <div class="column">
                <hr class="bg-is-electric-blue" style="height: 2px; margin: 0;">
            </div>
            <div class="column">
                <hr class="bg-is-electric-blue" style="height: 2px; margin: 0;">
            </div>
            <div class="column">
                <hr class="bg-is-electric-blue" style="height: 2px; margin: 0;">
            </div>
            <div class="column">
                <hr class="bg-is-electric-blue" style="height: 2px; margin: 0;">
            </div>
        </div>

        <!-- Tokenized words -->
        <div class="columns is-gapless is-multiline has-text-centered">
            ${htmlTokens}
        </div>

        <hr style="border: 1px dashed #20aaeb">

        <!-- Selected Positive Keywords -->
        <p class="is-electric-blue selected-positive-keywords-label" hidden>Add Positive Keywords to your Campaign</p>
        <div class="mb-3 selected-positive-keywords">
        </div>

        <!-- Selected Negative Keywords -->
        <p class="has-text-danger selected-negative-keywords-label" hidden>Add Negative Keywords to your Campaign</p>
        <div class="mb-3 selected-negative-keywords">
        </div>

        <div class="has-text-right mt-5">
            <button class="button is-electric-blue is-small" onclick="console.log(getSelectedKeywords(this))">
                Add To Campaigns
            </button>
        </div>

    </div>

`
    parent.classList.add('is-active')
    parent.append(newElem)

}

function selectPositiveKeyword(elem) {

    let chosenKeyword = elem.parentNode.previousElementSibling.innerText

    let container = elem.closest(".keywords-popup")

    let positiveArray = getSelectedPositiveKeywords(container)
    let negativeArray = getSelectedNegativeKeywords(container)

    if (positiveArray.includes(chosenKeyword)) {
        console.log(chosenKeyword, 'has already been added to positive keywords')
        return false;
    } else if (negativeArray.includes(chosenKeyword)) {
        alert(`"${chosenKeyword}" has already been added as a negative keyword. It cannot be both negative and positive.`)
        return false;
    }

    container.getElementsByClassName("selected-positive-keywords-label")[0].hidden = false

    let selectedPositiveKeywords = container.getElementsByClassName("selected-positive-keywords")[0]

    let newElem = document.createElement('span')
    newElem.innerHTML = `
            <span>${chosenKeyword}</span>
            <span class="icon ml-0 mr-1 is-electric-blue">
                <i class="fas fa-trash-alt is-clickable" onclick="removeSelectedKeyword(this)"></i>
            </span>`
    newElem.classList.add('icon-text')
    selectedPositiveKeywords.appendChild(newElem)

}

function selectNegativeKeyword(elem) {

    let chosenKeyword = elem.parentNode.previousElementSibling.innerText

    let container = elem.closest(".keywords-popup")

    let negativeArray = getSelectedNegativeKeywords(container)
    let positiveArray = getSelectedPositiveKeywords(container)

    if (negativeArray.includes(chosenKeyword)) {
        console.log(chosenKeyword, 'has already been added to negative keywords')
        return false
    } else if (positiveArray.includes(chosenKeyword)) {
        alert(`"${chosenKeyword}" has already been added as a positive keyword. It cannot be both negative and positive.`)
        return false
    }

    container.getElementsByClassName("selected-negative-keywords-label")[0].hidden = false

    let selectedNegativeKeywords = container.getElementsByClassName("selected-negative-keywords")[0]

    let newElem = document.createElement('span')
    newElem.innerHTML = `
            <span>${chosenKeyword}</span>
            <span class="icon ml-0 mr-1 is-electric-blue">
                <i class="fas fa-trash-alt is-clickable" onclick="removeSelectedKeyword(this)"></i>
            </span>`
    newElem.classList.add('icon-text')
    selectedNegativeKeywords.appendChild(newElem)

}

function getSelectedPositiveKeywords(container) {
    let selectedPositiveKeywords = container.getElementsByClassName("selected-positive-keywords")[0].children
    let returnArray = []
    for (let i = 0; i < selectedPositiveKeywords.length; i++) {
        returnArray.push(selectedPositiveKeywords[i].firstElementChild.innerText)
    }
    return returnArray
}

function getSelectedNegativeKeywords(container) {
    let selectedNegativeKeywords = container.getElementsByClassName("selected-negative-keywords")[0].children
    let returnArray = []
    for (let i = 0; i < selectedNegativeKeywords.length; i++) {
        returnArray.push(selectedNegativeKeywords[i].firstElementChild.innerText)
    }
    return returnArray
}

function getSelectedKeywords(elem) {

    let container = elem.closest(".keywords-popup")

    let positiveKeywordArray = getSelectedPositiveKeywords(container)
    let negativeKeywordArray = getSelectedNegativeKeywords(container)

    fetch("{{ url_for('api_campaigns.add_campaign_keywords') }}", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'campaignId': campaignId,
                'keywords': {
                    positive: positiveKeywordArray,
                    negative: negativeKeywordArray
                }
            })
        }
    )
        .then((response) => response.json())
        .then((data) => {
            console.log('Add keywords (response):', data)
            container.remove()
            parent.classList.remove('is-active')
            alert('Keywords added to campaign. Campaign may take a minute to update.')
        })

    return {
        "positive": positiveKeywordArray,
        "negative": negativeKeywordArray
    }

}

function removeSelectedKeyword(elem) {

    let container = elem.closest(".keywords-popup")

    let positiveKeywordCount = container.getElementsByClassName("selected-positive-keywords")[0].childElementCount
    container.getElementsByClassName("selected-positive-keywords-label")[0].hidden = positiveKeywordCount <= 1

    let negativeKeywordCount = container.getElementsByClassName("selected-negative-keywords")[0].childElementCount
    container.getElementsByClassName("selected-negative-keywords-label")[0].hidden = negativeKeywordCount <= 1

    elem.parentElement.parentElement.remove()

}

function closeWindow(elem) {
    // elem.closest(".keywords-popup").remove()
    document.getElementById('keyword-modal').classList.remove('is-active')
}
