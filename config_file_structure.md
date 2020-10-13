# Configuration file structure

for searchhelper.py

All keys may be omitted except where indicated.
See [example.yaml](./example.yaml) as a reference.

* **Application Title**  
  _Title displayed in the window titlebar._
* **Description**  
  _Medium-long description of the application, is displayed in the upper half of the program window._
* **Metadata**  
  _Metadata for the configuration file. All subkeys and their values will be displayed in the "About..." window._  
  Recommended subkeys:
  * **Author**
  * **Date** _in YAML files, enclose the date in single quotes to ensure the value is interpreted as a string_
  * **Version** _(single quoted)_
* **Search URLs**  
  _This is the only **required top-level key**._  
  * Each subkey of this represents a **URL category.**  
    Each URL category **must have** one of the following subkeys:
    * **URL**  
      _directly specifying the single URL in this category_
    * **URLs**  
      _followed by a key-value list of URL names/identifiers and URLs in this category._

    Additionally, the following subkeys are allowed in a category:
    * **Number Format**  
      _If the expected search string for this category is an integer,
      you can use this subkey to specify a Python format string
      (see [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec)
      in the Python Standard Library Reference), e.g. ```'>08d'``` for an 8-digit
      number with leading zeroes._  
      Please be aware that non-numeric inputs will cause an error message if a number format is specified.
    * **Search Term Must Match**  
      _If you specify a regular expression here, the search term is matched against this regular expression
      and causes an error message if it does not match the expression.
      Errors in the regular expression will also cause an error message.  
      Matching is only performed if no **Number Format** (see above) was specified._
    * **Regex Description**  
      _Description of the format expected by the regular expression specified using **Search Term Must Match**.
      If the search term does not match the regular expression, this description is presented along
      with the error message._
    * **Preferred Browser**  
      _If specified and a registered web browser with that key exists, open the URL(s) from this category
      in that browser instead of the standard browser._
* **Deviant Homepages**  
  _If the search term is empty, the home pages of the URLs instead of the search pages are opened.  
  Normally, the home page is derived from each URL by simply omitting the path part, which ought to be
  sufficient in most cases.  
  For all other cases, you can specify a deviant home page for each
  one-URL-category using the category name as key, or for each URL of a multiple-URL-category
  using the URL name/identifier as the key._
* **Options**  
  The following options are recognized:
  * **Mutually Exclusive Categories**  
    _If set to ```true```, categories are displayed with radiobuttons instead of checkboxes,
    so only one catgory can be selected at the same time._
  * **Register Browsers**  
    _Register web browsers for the **Preferred Browser** category option._  
    Note: Browsers are only registered if there is not already a browser registered with that name
    (automatically by the [webbrowser module](https://docs.python.org/3/library/webbrowser.html))
    and if the specified executable path exists._
  * **Special Select Keys**  
    _Here, you can add key combinations as documented at <https://tkdocs.com/shipman/event-modifiers.html>
    that will be used to select multiple categories at once._  
    Every key combination **must have** the following two subkeys:
    * **Label**  
    _A summary for the group of categories that is selected by the key combination_
    * **Categories**  
    _The list of category names to be selected.
    Each name not matching a defined category name (i.e. a **Search URLs** subkey) will be ignored._
* **Translations**  
  _Translations for the GUI (key-value-pairs).
  For any omitted translation, a default value will be used._  
  See the example files for translations.

