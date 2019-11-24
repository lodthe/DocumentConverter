package client.web

enum class Format(
    val serverName: String,
    val displayName: String,
    val extensions: List<String>
) {

    MD(serverName = "markdown", displayName = "Markdown", extensions = listOf("md")),
    HTML(serverName = "html", displayName = "HTML", extensions = listOf("html", "htm")),
    DOCX(serverName = "docx", displayName = "MS Word Document", extensions = listOf("docx")),
    ODT(serverName = "odt", displayName = "Open Office Document", extensions = listOf("odt")),
    PLAIN(serverName = "plain", displayName = "Plain text", extensions = listOf("txt")),
}

internal const val INPUT_FILE_ID = "input_file"
internal const val DIV_FORMATS_ID = "div_formats"
internal const val INPUT_FORMAT_NAME = "input_format_name"
