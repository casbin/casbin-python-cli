def process_line_breaks(text):  
    """Handle line breaks in strings"""  
    if text is None:  
        return None  
    return text.replace('\\n', '\n')