

let Global = {
    selectedProfile: ""
}

let GlobalProfiles = {}



window.addEventListener("load", () => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const socket = io(urlParams.get('ws'));

    socket.on('connect', () => {
        socket.emit('fetch_profiles_data')
    })

    socket.on('profiles', (data) => {
        GlobalProfiles = data["profiles"]
        SetupControls(GlobalProfiles)
        UpdateButtons()
    })
    CreateButtons(socket)
})
