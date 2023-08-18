# ignore javascript & css

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

def fetch_url():
    url = url_entry.get()
    try:
        response = requests.get(url)
        parsed_html = html5lib.parse(response.text)
        
        # Remove <script> tags
        parsed_html = remove_script_tags(parsed_html)
        
        # Remove <style> and <link rel="stylesheet"> tags
        parsed_html = remove_style_tags(parsed_html)
        
        # This will just get the text of the webpage, without any formatting
        content = ''.join([text for text in parsed_html.itertext()])
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


