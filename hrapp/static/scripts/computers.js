const infoDialog = document.querySelector(".infoDialog")
const message = document.querySelector(".infoDialog__message")
const closeDialog = document.querySelector(".closeDialog")

document.querySelector(".computers").addEventListener("click", (evt) => {
    if (evt.target.id.startsWith("detail")) {
        const id = evt.target.id.split("--")[1]
        message.innerText = 'Are you sure you want to delete this computer? This is irreversable and could cost you your job.'
        infoDialog.show()
    }
})

// Close the dialog when the escape key is pressed
window.addEventListener("keyup", e => {
    if (e.keyCode === 27) {
        infoDialog.close()
    }
})
