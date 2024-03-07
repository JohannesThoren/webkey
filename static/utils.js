function GetListOfProfiles(profiles) {
    let listOFProfiles = []

    for (let key in profiles)
        listOFProfiles.push(key)

    return listOFProfiles
}
