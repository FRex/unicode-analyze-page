# Unicode Analyze Page

A simple website where you type in a string and get a list of all Unicode characters in it.

To see it in action go to [https://frex.github.io/unicode.html](https://frex.github.io/unicode.html).

To deploy this tool yoursef you need the two files:
1. `index.html` - the HTML with input box and inline JS to analyze the string.
2. `data.js` - the data as JSON, generated from `UCD.zip` and `Unihan.zip` files.

Both files and the `gendata.py` script that generates `data.js` are in this repo.

To get the `UCD.zip` and `Unihan.zip` files, visit
[https://www.unicode.org/Public/UCD/latest/ucd/](https://www.unicode.org/Public/UCD/latest/ucd/).

You don't need to unpack them, just drop them in same directory as `gendata.py`
and run it, to generate `data.js`.
