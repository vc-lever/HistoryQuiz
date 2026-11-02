async function onSubmitButton()
{
    const form = document.getElementById("submit_form")
    if (!form.reportValidity()) {
        return
    }

    const formJSON = Object.fromEntries(new FormData(form).entries())
    console.log(formJSON)
    const statusMessage = document.getElementById("submit_status")

    try {
        const response = await fetch("/api/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formJSON)
        })
        const result = await response.json()
        const message = result.error || result.message
        statusMessage.textContent = `Status ${response.status}${message ? `: ${message}` : ""}`
    } catch (error) {
        statusMessage.textContent = `Request failed: ${error.message}`
    }
}


function onLoadDocument()
{
    document.getElementById("submit_button").addEventListener("click", onSubmitButton)
}

document.addEventListener("DOMContentLoaded", onLoadDocument)