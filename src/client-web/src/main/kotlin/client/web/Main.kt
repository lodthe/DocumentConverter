package client.web

import kotlinx.html.*
import kotlinx.html.dom.append
import kotlinx.html.js.input
import kotlinx.html.js.onClickFunction
import org.w3c.dom.HTMLAnchorElement
import org.w3c.dom.HTMLDivElement
import org.w3c.dom.HTMLInputElement
import org.w3c.dom.asList
import org.w3c.dom.events.Event
import org.w3c.dom.url.URL
import org.w3c.fetch.RequestInit
import org.w3c.xhr.FormData
import kotlin.browser.document
import kotlin.browser.window
import kotlin.dom.clear

private fun showMessage(message: String) {
    window.alert(message)
}

private fun onConvertButtonClicked(event: Event) {
    val formatsDiv = document.getElementById(DIV_FORMATS_ID) as HTMLDivElement

    val checkedFormat = formatsDiv
        .getElementsByTagName("input")
        .asList()
        .mapNotNull { it as? HTMLInputElement }
        .singleOrNull(HTMLInputElement::checked)

    if (checkedFormat == null) {
        showMessage("Please select a format")
        return
    }

    val fileInput = document.getElementById(INPUT_FILE_ID) as HTMLInputElement

    val file = fileInput.files?.asList()?.singleOrNull()

    if (file == null) {
        showMessage("Please select a single file")
        return
    }

    val formData = FormData().apply {
        append("file", file)
    }

    val format = checkedFormat.value.toIntOrNull()?.let { Format.values().getOrNull(it) }

    if (format == null) {
        showMessage("HTML is broken, please reload the page")
        return
    }

    val conversionUrl = "/convert/${format.serverName}"
    console.log("Sending file ${file.name} to $conversionUrl")

    window
        .fetch(
            input = conversionUrl,
            init = RequestInit(
                method = "POST",
                body = formData
            )
        )
        .then { response ->
            when (response.status) {
                200.toShort() -> response.blob().then { blob ->
                    val url = URL.createObjectURL(blob)

                    val tempLink = (document.createElement("a") as HTMLAnchorElement).apply {
                        style.display = "none"
                        href = url
                        download = "${file.name}.${format.extensions.first()}"
                        innerHTML = "a"
                    }

                    document.body!!.appendChild(tempLink)

                    tempLink.click()

                    URL.revokeObjectURL(url)
                    tempLink.remove()
                }

                else -> response.text().then { text ->
                    val errorText = text.substringAfterLast("<p>").substringBefore("</p>")
                    showMessage("Server error: $errorText")
                    console.log(text)
                }
            }
        }
}

private fun createContent() {
    val ui = document.getElementById("ui") as HTMLDivElement

    ui.clear()

    ui.append {
        p { text("Choose a file:") }
        input(type = InputType.file) { id = INPUT_FILE_ID }
        p { text("Select an output format:") }
        div {
            id = DIV_FORMATS_ID

            Format.values().forEachIndexed { i, format ->
                label {
                    input(type = InputType.radio, name = INPUT_FORMAT_NAME) {
                        value = i.toString()

                        if (i == 0) {
                            checked = true
                        }
                    }
                    text("${format.displayName} (${format.extensions.first()})")
                }

                br()
            }
        }
        br()
        button {
            onClickFunction = ::onConvertButtonClicked

            text("Convert!")
        }
    }
}

fun onLoad() {
    createContent()
}
