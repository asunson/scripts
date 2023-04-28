#!/usr/bin/env python

import requests
import re
import webbrowser
import os

with open("./style_numbers.txt", "r") as input_file:
    contents = input_file.read()

style_numbers = contents.split("\n")
img_pattern = re.compile('<img [^>]*src="([^"]+)')

output = {}
missing_numbers = []
for style_number in style_numbers:
    print(f"Looking for image for {style_number}")
    r = requests.get(f"https://www.dkny.com/catalogsearch/result/?q={style_number}")
    raw_html = r.text
    images = img_pattern.findall(raw_html)
    matches = [i for i in images if style_number in i]
    if len(matches) > 0:
        print(f"Found a url for {style_number}!")
        output[style_number] = matches
    else:
        print(f"-----UH OH----- Could not find an image for {style_number}")
        missing_numbers.append(style_number)

html_head = """<html style="font-family: system-ui;background-color: lavender">
<head><title>Style Number Handbook</title></head>
<h1 style="text-align: center;margin-block:0">Welcome Alicia!</h1>
<p style="text-align: center;margin-block:0">...to your new style number handbook</p>
"""

html_missing_numbers = f'<p style="background-color: ivory;padding: 8px;">Could not find images for: {", ".join(missing_numbers)}</p>' if len(missing_numbers) > 0 else ""

html_table_head = """
<table style="margin:auto;margin-top:16px;border-collapse: collapse;border: 1px solid black;">
<tbody>
<tr>
<th style="text-align: center;padding: 8px 16px;border: 1px solid black;">Style Number</th>
<th style="border: 1px solid black;">URL</th>
</tr>
"""  

html_table_contents = "\n".join(
    [
        f'<tr><td style="text-align: center;font-weight: 700;border: 1px solid black;">{number}</td><td style="padding: 16px;border: 1px solid black;"><img src={url[0]}></img></td></tr>' for number, url in output.items()
    ]
)

html_table_tail = """</tbody>
</table>
"""

html_tail = """
</body>
</html>
"""


html = html_head + html_missing_numbers + html_table_head + html_table_contents + html_table_tail + html_tail

with open('style_number_urls.html', 'w') as f:
    f.write(html)

print("Successfully generated an style_number_urls.html")
print(f"Missing images for: {missing_numbers}")
filepath = os.getcwd()
file_uri = 'file:///' + filepath + '/style_number_urls.html'
webbrowser.get().open(file_uri)