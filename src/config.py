# File extension aliases
TYPE_ALIAS = {
    'htm': 'html',
    'html': 'html',
    'docx': 'docx',
    'markdown': 'markdown',
    'odt': 'odt',
    'bat': 'markdown',
    'txt': 'markdown',
    'plain': 'plain',
}

# Conversion: key = input format, value = available output formats
AVAILABLE_CONVERSIONS = {
    'html': ('html', 'markdown', 'plain'),
    'markdown': ('markdown', 'html', 'plain'),
    'docx': ('docx', 'html', 'markdown', 'plain'),
    'odt': ('odt', 'html', 'markdown', 'plain'),
}