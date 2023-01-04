function getCampaignDetails(elem) {
    let rowElement = elem.parentNode.parentNode
    let campaignID = rowElement.getAttribute('data-campaign-id')
    let campaignName = rowElement.getAttribute('data-campaign-name')
    return {
        'id': campaignID,
        'name': campaignName
    }
}

function deleteCampaign(elem, isActive) {
    if (isActive === "True") {
        alert('Please pause the campaign before deleting.')
    } else {
        let data = getCampaignDetails(elem)
        fetch('{{ url_for("api_campaigns.delete_campaign") }}', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'campaignID': data['id'],
                'campaignName': data['name'],
            })
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                window.location.reload()
            })
    }
}