let signupModal = document.getElementById('signup-modal')

// This script handles the transitioning between each step of the signup sequence
function stepTransition(elem = undefined, nextStepId = undefined) {
    signupModal.classList.add('is-active')
    if (elem != undefined) {
        while (elem.classList.contains('signup-step') !== true) {
            elem = elem.parentNode
        }

        elem.classList.add('hidden')  // Hiding the old step

        if (nextStepId === undefined) {
            nextStepId = elem.getAttribute('data-next-step')
        }
    }

    if (nextStepId === 'none') {
        // document.getElementById('signup-modal').classList.remove('is-active')
        window.location.href = "{{ url_for('index') }}"
    }
    // TODO remove next two lines to restore create account section
    else {
        if (nextStepId === 'signup-step-1') {
            nextStepId = 'signup-step-1-login'
        }
    }

    let nextStepElem = document.getElementById(nextStepId)
    nextStepElem.classList.remove('hidden')  // Revealing the next step
}