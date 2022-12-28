function create_link(data, base = window.location.href) {

    let urlString = base.split('?')
    base = urlString[0]
    let paramsString = urlString[1]
    let searchParams = new URLSearchParams(paramsString);

    // searchParams.has("name") === true; // true
    // searchParams.get("age") === "1337"; // true

    for (let [key, value] of Object.entries(data)) {
        console.log(key, value);
        searchParams.set(key, String(value))
    }

    let URL = base + '?' + searchParams.toString()

    console.log('Returned URL:', URL)

    return URL
}
