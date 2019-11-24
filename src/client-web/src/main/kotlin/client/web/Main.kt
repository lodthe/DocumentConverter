package client.web

import kotlinx.html.*
import kotlinx.html.dom.append
import kotlinx.html.js.input
import kotlinx.html.js.onChangeFunction
import kotlinx.html.js.onClickFunction
import org.w3c.dom.HTMLAnchorElement
import org.w3c.dom.HTMLDivElement
import org.w3c.dom.HTMLInputElement
import org.w3c.dom.asList
import org.w3c.dom.url.URL
import org.w3c.fetch.RequestInit
import org.w3c.files.File
import org.w3c.xhr.FormData
import kotlin.browser.document
import kotlin.browser.window
import kotlin.dom.clear
import kotlin.js.Json

private val ui get() = document.getElementById(DIV_UI_ID) as HTMLDivElement
private val footer get() = document.getElementById(DIV_FOOTER_ID) as HTMLDivElement
private val fileInput get() = document.getElementById(INPUT_FILE_ID) as HTMLInputElement

private lateinit var availableServerConversions: Map<String, List<String>>

private fun showMessage(message: String) {
    window.alert(message)
}

private fun onConvertButtonClicked(file: File) {
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

    val formData = FormData().apply {
        append("file", file)
    }

    val format = checkedFormat.value.toIntOrNull()?.let { Format.values().getOrNull(it) }

    if (format == null) {
        showMessage("HTML is broken, please reselect the file")
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
                        // TODO: is there a way to get a correct filename from the server?
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

private fun showUnsupportedFileExtension(fileExtension: String) {
    val supported = availableServerConversions
        .keys
        .flatMap { serverName ->
            Format.values().single { serverName == it.serverName }.extensions
        }
        .toSet()

    footer.apply {
        clear()

        append {
            p { text("File extension $fileExtension is unsupported. Supported ones: ${supported.joinToString()}") }
        }
    }
}

private fun askForSingleFile() {
    footer.apply {
        clear()

        append {
            p { text("Please select a single file") }
        }
    }
}

private fun onFileSelected() {
    val file = fileInput.files?.asList()?.singleOrNull()

    if (file == null) {
        askForSingleFile()
        return
    }

    val fileExtension = file.name.substringAfterLast(".", missingDelimiterValue = "")
    val serverConversionName = Format.values().firstOrNull { fileExtension in it.extensions }?.serverName

    if (serverConversionName == null || serverConversionName !in availableServerConversions) {
        showUnsupportedFileExtension(fileExtension)
    } else {
        showAvailableFileConversions(serverConversionName, file)
    }
}

private fun showAvailableFileConversions(fileExtensionServerName: String, file: File) {
    val availableFormats = availableServerConversions.getValue(fileExtensionServerName)
    console.log("Available conversions for selected file: ${availableFormats.joinToString()}")

    var first = true

    footer.apply {
        clear()

        append {
            p { text("Select an output format:") }
            div {
                id = DIV_FORMATS_ID

                Format.values().forEachIndexed { i, format ->
                    if (format.serverName in availableFormats) {
                        label {
                            input(type = InputType.radio, name = INPUT_FORMAT_NAME) {
                                value = i.toString()

                                if (first) {
                                    checked = true
                                    first = false
                                }
                            }
                            text("${format.displayName} (${format.extensions.first()})")
                        }

                        br()
                    }
                }
            }
            br()
            button {
                onClickFunction = { onConvertButtonClicked(file) }

                text("Convert!")
            }
        }
    }
}

private fun createContent() {
    ui.apply {
        clear()

        ui.append {
            p { text("Choose a file:") }
            input(type = InputType.file) {
                id = INPUT_FILE_ID
                onChangeFunction = { onFileSelected() }
            }
            div { id = DIV_FOOTER_ID }
        }
    }
}

private fun createConverionsAreUnavailable() {
    ui.apply {
        clear()

        append {
            p { text("Can't retrieve available conversion formats...") }
        }
    }
}

private fun createIncompatibleClient() {
    ui.apply {
        clear()

        append {
            p { text("The client version is incompatible") }
        }
    }
}

fun saveAvailableServerConversions(serverConversionsJson: String) {
    availableServerConversions = mutableMapOf<String, List<String>>().also { conversions ->
        val json = JSON.parse<Json>(serverConversionsJson)

        for (key: String in js("Object").keys(json)) {
            val value = json[key]
            val serverFormats = (value as? Array<*>)?.mapNotNull { it as? String }?.toList()

            if (serverFormats != null) {
                conversions[key] = serverFormats
            } else {
                console.log("Skipping bad key-value in available conversions: $key :: $value")
            }
        }
    }

    val clientConversionNames = Format.values().map(Format::serverName).toSet()

    fun Iterable<String>.isUnsupportedByClient() = any { it !in clientConversionNames }

    val unsupportedKeys = availableServerConversions.keys.isUnsupportedByClient()
    val unsupportedValues = availableServerConversions.values.any(Iterable<String>::isUnsupportedByClient)
    if (unsupportedKeys || unsupportedValues) {
        console.log("Incompatible client detected:")
        console.log("Client conversion names: ${clientConversionNames.joinToString()}")
        console.log("Server conversion names: $availableServerConversions")

        createIncompatibleClient()
    } else {
        createContent()
    }
}

@Suppress("unused")
fun onLoad() {
    window
        .fetch(input = "/get_available_conversions")
        .then { response ->
            when (response.status) {
                200.toShort() -> response.text().then { text ->
                    saveAvailableServerConversions(text)
                }

                else -> createConverionsAreUnavailable()
            }
        }
}
