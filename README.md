# Search helper

Python script using a Tk GUI for opening predefined search URLs in the web browser.

## Prerequisites

* Requires Python 3.6 or greater.
* PyYAML is required for YAML configuration file parsing.

## Invocation

Choose the configuration file via a dialog:
```
python3 searchhelper.py
```

Use a YAML configuration file (preferred, but requires PyYAML to be installed):
```
python3 searchhelper.py configfile.yaml
```

Use a JSON configuration file
```
python3 searchhelper.py configfile.json
```

## User interface

![UI on Windows using example.yaml](./example-screenshot.png)

When you have entered a search string, you can open it in the selected
category or categories using the "Open" button or the **Return** key.
This will open the URLs of each category in webbrowser tabs.
If possible, each category is opened in a separate browser window.

The first up to 12 category selections can be toggled using the function keys
as displayed (**F1** through **F12** from top down).

Pressing **Escape** or clicking the "Quit" button exits the program.

You can delete the search term by pressing **Control-D** or by clicking
the "Clear" button. **Control-X** will copy the search term to the clipboard
and then clear the search term entry field.

For single-URL categories, the "Copy URL" button will copy a URL
(which is generated from the search term in combination with the category
written before the button) to the clipboard.

Categories with multiple URLs have a "List URL names" button instead.
Clicking on that button will open a popup window containing a list of all
URL names/identifiers that belong to the category written before the button.

Other key combinations selecting multiple categories can be configured
in the configuration files. In the example above
(which uses [example.yaml](./example.yaml)), that is **Control-Shift-A**
selecting the first and third category.

## Configuration files

The configuration file can be in YAML or JSON format.
It contains a data structure as described in
[config\_file\_structure.md](./config_file_structure.md).

The [configfile.py script](./configfile_script.md) can be used to compare configuration files
or to convert a YAML configuration file to a JSON configuration file.
Additionally, it is imported by the main script to load the files.

