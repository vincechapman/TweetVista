// This script calls an api endpoint that checks if any user credentials are saved in the flask session object
fetch('{{ url_for("api_auth.check_if_logged_in") }}', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then((response) => response.json())
    .then((data) => {
        if (data['status'] === 200) {
            console.log(`${data['message']}: ${data['data']}`)
        } else {
            console.log(data['message'])
            stepTransition(undefined, 'signup-step-1')
        }
    })
