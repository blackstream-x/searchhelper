# Search helper

Python script using a Tk GUI for opening predefined search URLs in the web browser.

## Prerequisites

* Requires Python 3.6 or greater.
* PyYAML is required for YAML configuration file parsing.

## Usage

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

## Configuration files

The configuration file can be in YAML or JSON format.
It contains a data structure as described in
[config\_file\_structure.md](./config_file_structure.md).

For some examples, see the .json and .yaml files in this directory.

The [configfile.py](./configfile.py) script can be used to compare configuration files
or to convert a YAML configuration file to a JSON configuration file.
Additionally, it is imported by the main script to load the files.

