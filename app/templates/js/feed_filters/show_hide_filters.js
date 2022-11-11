// Event listener
let filterDropdowns = document.querySelectorAll('.button.campaign-filter')
for (let i = 0; i < filterDropdowns.length; i++) {
    filterDropdowns[i].addEventListener("click", dropdownClicked)
}

// This hides the filter fields when user clicks elsewhere on page
window.onclick = function(event) {
    let clickedElem = event.target
    let dropDown = clickedElem.closest('.dropdown-trigger')
    if (!dropDown) {
        hideCampaignFilterFields()  // TODO Update this so that the popups themselves don't disappear when user clicks on them
    }
}

// On click
function dropdownClicked() {
    hideCampaignFilterFields()
    showCampaignFilterField(this)
}

// Hide all campaign fields
function hideCampaignFilterFields() {
    hideAllArrows()
    let filterFields = document.querySelectorAll('div.campaign-filter-field')
    for (let i = 0; i < filterFields.length; i++) {
        filterFields[i].hidden = true
    }
}

// Display chosen campaign fields
function showCampaignFilterField(elem) {
    showArrow(elem)
    let fieldId = elem.getAttribute('data-field')
    document.getElementById(fieldId).hidden = false
}

// Updating double arrow icon
function hideAllArrows() {
    let icons = document.querySelectorAll('.button.campaign-filter')
    for (let i = 0; i < icons.length; i++) {
        let span = icons[i].parentNode.parentNode.lastElementChild
        span.style.display = 'none'
    }
}

// Showing arrow for selected field
function showArrow(elem) {
    let span = elem.parentNode.parentNode.lastElementChild
    span.style.display = 'inline-flex'
}

