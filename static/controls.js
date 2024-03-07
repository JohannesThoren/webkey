function _OnChangeProfile() {
    
}

function SetupControls(profiles) {
    let profilesList = GetListOfProfiles(profiles)
    let profileSelect = document.querySelector("#profile-select")

    profilesList.forEach(profile => {

        console.log(profile)
        let option = document.createElement("option")
        option.setAttribute("value", profile)
        option.innerText = profile
        profileSelect.appendChild(option)
        
        
    })


    profileSelect.addEventListener("change", (e) => {
        Global.selectedProfile = profileSelect.options[profileSelect.selectedIndex].value
        UpdateButtons()
    })

    Global.selectedProfile = profilesList[0]
}