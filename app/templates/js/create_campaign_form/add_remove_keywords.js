function addKeyword(rowNumber, parentID, elem = undefined) {

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
            <input name="${parentID}|${rowNumber}|keyword" type="text" class="input" placeholder="Enter keyword">
        </div>

        <div class="column is-narrow-desktop">
            <div class="field">
                <div class="control">
                    <div class="select is-fullwidth">
                        <select name="${parentID}|${rowNumber}|type" class="is-fullwidth" required>
                            <option>Exact Order</option>
                            <option>Any Order</option>
                            <option>Hashtag</option>
                            <option>Handle</option>
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
