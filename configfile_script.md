# configfile.py script

_A utility script for JSON and YAML configuration file handling_

This script serves two purposes:
1. It is imported as a module by the [main program](./README.md) to read the configuration files.
2. You can use it from the command line to compare or convert configuration files.

YAML capabilities are determined automatically,
depending on the result of importing the yaml module.

## Module interface

### Constants

configfile.**YAML\_SUPPORTED**

> YAML support flag. Contains ```True``` if the runtime environments supports YAML, ```False``` otherwise.

configfile.**SUPPORTED\_FILE\_TYPE**

> A mapping containing file type labels and tuples of possible file extensions.
> Always contains JSON, and additionally YAML if suported.

configfile.**LOADERS**

> A mapping containing this module’s loader function for each supported file type.

configfile.**DUMPERS**

> A mapping containing this module’s dumper function for each supported file type.

### Exceptions

configfile.**FiletypeNotSupported**

> Raised if an unsupported or unknown file type was specified.

configfile.**InvalidFormatError**

> Raised if file content is not loadable
> (i.e. if the YAML or the JSON parser raised an exception)

### Functions

configfile.**load\_json**(_file\_name_)

> Loads data from the JSON file _file\_name_.
> Raises an **InvalidFormatError** on invalid (i.e. non-JSON) file contents.

configfile.**dump\_to\_json**(_data, file\_name_)

> Dumps _data_ to the JSON file _file\_name_.

configfile.**load\_yaml**(_file\_name_)

> Loads data from the YAML file _file\_name_.
> Raises an **InvalidFormatError** on invalid (i.e. non-YAML) file contents.  
> **Only defined if YAML is supported.**

configfile.**dump\_to\_yaml**(_data, file\_name_)

> Dumps _data_ to the YAML file _file\_name_.  
> **Only defined if YAML is supported.**

configfile.**read\_file**(_file\_name_)

> Loads data from the file _file\_name_, determining its type by the extension.
> Raises **FiletypeNotSupported** on unsupported file types.

configfile.**write\_to\_file**(_data, file\_name_)

> Dumps _data_ to the file _file\_name_, determining its type by the extension.
> Raises **FiletypeNotSupported** on unsupported file types.

configfile.**comparable\_form**(_data_)

> Returns a string containing a comparable. serialized form of data
> with sorted dict keys. If YAML is supported, that is YAML, else JSON.

## Command line interface

### Compare files

Invocation:

```
configfile.py [-v|--verbose] compare [--diff] file_name_1 file_name_2
```

Compares data from file\_name\_1 with data from file\_name\_2.

Exits with returncode 0 if data from both files are equal,
and with returncode 1 if they are different.

If the ```--diff``` option was provided, the script produces a
[unified diff](https://docs.python.org/3/library/difflib.html#difflib.unified_diff)
output of data from both files.  
Depending on the YAML capabilities of the runtime environment,
data is represented in YAML or JSON.

### Translate (convert) files

Invocation:

```
configfile.py [-v|--verbose] translate [--overwrite] input_file_name output_file_name
```

Translates data from input\_file\_name to output\_file\_name. The file formats
are determined from the file extensions.

Exits with returncode 2 if the output file already exists
and no ```--overwrite``` option was provided.
If the output file was written successfully, script exits with returncode 0.
