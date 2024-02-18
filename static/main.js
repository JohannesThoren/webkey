const global = {
    edit: false,
    currentProfile: null,
    profiles: []
}

var socket = io();

function Clear() {
    console.log("clear")
    global.profiles.forEach(profile => {
        if (profile.name == global.currentProfile) {
            let keyMap = profile["keyMap"]

            keyMap.forEach(mapping => {
                let tmp = document.querySelector(`button[data-id="${mapping.id}"]`)
                console.log(tmp)
                tmp.innerText = ""
                tmp.removeAttribute("data-action")
            })

        }
    })
}

function CreateProfileSelect() {
    let ps = document.querySelector("#profile-select")

    ps.addEventListener("change", (e) => {
        Clear()
        global.currentProfile = ps.options[ps.selectedIndex].value
        SetKeyMap()
    })


    let profiles = global.profiles
    console.log(profiles)

    profiles.forEach(profile => {
        let profileSelectOption = document.createElement("option")
        profileSelectOption.setAttribute("value", profile.name)
        profileSelectOption.innerText = profile.name
        ps.appendChild(profileSelectOption)
    })

    global.currentProfile = ps.options[ps.selectedIndex].value
}

function CreateButtonElement(id) {
    let b = document.createElement("button")
    b.setAttribute("data-id", id)
    b.className = "button"
    b.addEventListener("click", () => {
        if (b.getAttribute("data-action")) {
            socket.emit('click', { button: id, action: b.getAttribute("data-action") })
        }
    })
    return b;
}

async function SetupProfiles() {
    let resp = await fetch("/static/profiles.json")
    let jsonData = await resp.json()

    let profiles = jsonData["profiles"]

    profiles.forEach(profile => {
        global.profiles.push(profile)
    })

    console.log(profiles)
}


function SetKeyMap() {
    console.log("setting KeyMap")

    global.profiles.forEach(profile => {
        if (profile.name == global.currentProfile) {
            let keyMap = profile["keyMap"]


            keyMap.forEach(mapping => {
                let tmp = document.querySelector(`button[data-id="${mapping.id}"]`)
                tmp.innerText = mapping.text
                tmp.setAttribute("data-action", mapping.action)
            })

        }
    })
}

window.addEventListener("load", async () => {

    let gridElement = document.querySelector(".grid[data-type]")
    let type = gridElement.getAttribute("data-type")

    await SetupProfiles()

    SetGridSize(type, gridElement);

    CreateProfileSelect()

    SetKeyMap()

    socket.on('connect', function () {
        socket.emit('hello', { data: 'I\'m connected!' });
    });


})


function SetGridSize(type, gridElement) {
    switch (type) {
        case "7x5":
            for (let i = 0; i < 7 * 5; i++) {
                gridElement.appendChild(CreateButtonElement(i));
            }
            break;

        case "10x7":
            for (let i = 0; i < 10 * 7; i++) {
                gridElement.appendChild(CreateButtonElement(i));
            }
        default:
            break;
    }
}

