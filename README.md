# OneNote to Xournal++ Converter

This script is still a WIP, it converts OneNote pages from browser to editable Xournal++ compatible files.

## How to

1) Install the requirements
```Bash
pip3 install -r requirements.txt
```

2) Open the note that you want to convert from browser

3) Scroll the entire note to be sure that it's completely loaded

4) Using the developer tools find a `<div>` tag with WACViewPanel class and copy the inner HTML (the procedure may change according to the browser that you are using)
**Note: it may works even if you copy the inner HTML from `<body>`. The less HTML has to scan the higher are the probability of success**

5) Save the copied HTML to an HTML file. I suggest to save it in the same folder of the script

6) Launch the script
```Python
python3 ./onenote2xournal.py input_file.html output_file_name
```
**Note: the scripts do very few checks on the arguments, keep them as simple as possible**

## Why?
Because OneNote is **painfully slow** to open, especially when you open a large notebook shared with you and you can't export notes as PDF easily (if I remember correctly you need OneNote from the Office Suite to export PDF, otherwise you can't).

Also, having an offline copy of your notes is always a good thing :D

## Accuracy
It's not very accurate, I tried my best to keep everything in the right position. Sometimes you get very good result, sometimes you get something similar to a Picasso.

Further work is needed to align correctly the text boxes.

Tables are not supported by Xournal so they cannot be converted.
