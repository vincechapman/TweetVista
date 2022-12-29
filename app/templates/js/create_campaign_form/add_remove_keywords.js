
function prefillKeywordFields(prefillKeywords) {
    let currentRow
    for (let i = 0; i < prefillKeywords.length; i++) {
        currentRow = prefillKeywords[i]
        if (currentRow['type'] === 'positive') {
            addKeyword(1, 'positive-keywords-field', undefined, currentRow['text'], currentRow['order'])
        } else {
            addKeyword(1, 'negative-keywords-field', undefined, currentRow['text'], currentRow['order'])
        }
    }
}

function addKeyword(rowNumber, parentID, elem = undefined, prefillText = undefined, prefillOrder = undefined) {

    /* This function adds new rows to the keyword fields, provided the current row is not empty */

    // This is the parent element that contains all rows
    let parentElem = document.getElementById(parentID)

    if (elem) {
        let keywordRow = elem.closest('.keyword-row')
        console.log(keywordRow.querySelector('div.column > input').checkValidity())
    }

    // Change button to a bin
    if (elem) {
        elem.parentNode.innerHTML = "<img src=\"{{ url_for('static', filename='images/icons/Bin-Icon.jpg') }}\" alt='delete keyword' style='max-height: 40px' onclick='removeKeyword(this)'>"
    }

    // Row template
    let rowHTML = `
        <div class="column is-full-touch">
            <input name="${parentID}|${rowNumber}|keyword" type="text" class="input" placeholder="Enter keyword" value="${prefillText ? prefillText : ''}">
        </div>

        <div class="column is-narrow-desktop">
            <div class="field">
                <div class="control">
                    <div class="select is-fullwidth">
                        <select name="${parentID}|${rowNumber}|type" class="is-fullwidth" required>
                            <option ${prefillOrder === 'fixed' ? `selected` : ''}>Exact Order</option>
                            <option ${prefillOrder === 'none' ? `selected` : ''}>Any Order</option>
                            <option ${prefillOrder === 'hashtag' ? `selected` : ''}>Hashtag</option>  <!-- TODO Check this is correct -->
                            <option ${prefillOrder === 'handle' ? `selected` : ''}>Handle</option>  <!-- TODO Check this is correct -->
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <div class="column has-text-centered is-2 is-3-desktop">
            <button class="button is-electric-blue is-fullwidth" data-row-number="${rowNumber}" onclick="addKeyword(${rowNumber + 1}, '${parentID}', this);">+ Keyword</button>
        </div>
    `

    // Create new html element using row template
    let newNode = document.createElement('div')
    newNode.innerHTML = rowHTML
    newNode.classList.add('columns', 'is-vcentered', 'keyword-row', 'is-multiline')

    // Appends new html element
    parentElem.appendChild(newNode)
}

function removeKeyword(elem) {
    elem.closest('.keyword-row').remove()
}
