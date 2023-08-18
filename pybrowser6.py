# Switched libraries to BeautifulSoup to display only human-readable text
# Add a new line after elements that represent the ends of sections for better readability

import requests
import tkinter as tk
from tkinter import scrolledtext
from bs4 import BeautifulSoup

def extract_readable_text(html_content):
    """
    Uses BeautifulSoup to extract human-readable text from the given HTML content,
    and adds new lines for better readability.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script, style, meta, link, and noscript elements
    for script in soup(["script", "style", "meta", "link", "noscript"]):
        script.extract()
    
    # Add new lines after certain elements for better readability
    for element in soup.find_all(['br', 'p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        element.append('\n')
    
    # Get text, ensuring multiple spaces and newlines are turned into single spaces
    text = '\n'.join(soup.stripped_strings)
    return text

def fetch_url():
    url = url_entry.get()
    try:
        response = requests.get(url)
        
        # Extract and clean up text content
        content = extract_readable_text(response.text)
        
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
