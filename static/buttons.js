let buttons = []

function CreateButtons(socket) {
    let buttonsContainer = document.querySelector("#buttons-container")
    for(let i = 0; i < 28; i++) {
        let btn = document.createElement("button")
        btn.className="btn"
        btn.setAttribute("data-id", i)
        btn.addEventListener("click", () => {
            socket.emit("click", {"button": i, "profile": Global.selectedProfile})
        })
        buttonsContainer.appendChild(btn)
        buttons.push(btn)
    }
}


function UpdateButtons() {
    let mappings = GlobalProfiles[Global.selectedProfile]["mappings"]
    console.log(mappings)
    buttons.forEach(btn => {
        let id = btn.getAttribute("data-id")

        if(mappings[`${id}`])  {
            btn.innerText = mappings[`${id}`].text
        }
        else {
            btn.innerText = ""
        }

    })
}