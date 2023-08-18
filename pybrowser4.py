# display only human-readable text, ignoring source code, scripts, styles, and non-visible elements.

import requests
import tkinter as tk
from tkinter import scrolledtext
import html5lib

def remove_script_tags(parsed_html):
    """
    Removes <script> elements from the parsed HTML.
    """
    for script in parsed_html.findall(".//script"):
        script.getparent().remove(script)
    return parsed_html

def remove_style_tags(parsed_html):
    """
    Removes <style> elements and external stylesheet <link> tags from the parsed HTML.
    """
    # Remove <style> tags
    for style in parsed_html.findall(".//style"):
        style.getparent().remove(style)
    
    # Remove external stylesheets referenced via <link> tags
    for link in parsed_html.findall(".//link"):
        if link.attrib.get('rel') == ['stylesheet'] or 'css' in link.attrib.get('href', ''):
            link.getparent().remove(link)
            
    return parsed_html

def remove_non_visible_elements(parsed_html):
    """
    Removes elements that aren't typically visible on the rendered page.
    """
    # Remove <meta> tags
    for meta in parsed_html.findall(".//meta"):
        meta.getparent().remove(meta)

    # Remove <noscript> tags
    for noscript in parsed_html.findall(".//noscript"):
        noscript.getparent().remove(noscript)

    # Remove comments
    for elem in parsed_html.iter():
        if isinstance(elem, str):  # Comments are represented as strings
            if elem.startswith("<!--") and elem.endswith("-->"):
                if elem.getparent() is not None:
                    elem.getparent().remove(elem)

    return parsed_html

def fetch_url():
    url = url_entry.get()
    try:
        response = requests.get(url)
        parsed_html = html5lib.parse(response.text)
        
        # Remove <script>, <style>, <meta>, <noscript>, and comments
        parsed_html = remove_script_tags(parsed_html)
        parsed_html = remove_style_tags(parsed_html)
        parsed_html = remove_non_visible_elements(parsed_html)
        
        # Extract and clean up text content
        content = ''.join([text for text in parsed_html.itertext()])
        content = ' '.join(content.split())  # Removing excessive whitespace
        
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)
    except Exception as e:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"Error fetching URL: {e}")

root = tk.Tk()
root.title("Rudimentary Web Browser")

url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=10)
fetch_button = tk.Button(root, text="Fetch", command=fetch_url)
fetch_button.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=25)
text_area.pack(padx=10, pady=10)

root.mainloop()




