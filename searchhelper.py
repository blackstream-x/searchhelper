#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
searchhelper.py

Search URLs helper script with Tk GUI,
idea based on <https://antitext.de/suche.py> by @teh_aSak
"""


import os
import re
import sys
import textwrap
import time
import urllib.parse
import webbrowser

import tkinter
from tkinter import filedialog
from tkinter import messagebox

import configfile


#
# Constants
#

SCRIPT_NAME = 'Search Helper'
VERSION = '0.9.1'
HOMEPAGE = 'https://github.com/blackstream-x/searchhelper'
LICENSE = 'LICENSE.txt'
DEFAULT_CONFIG_FILE_NAME = 'example.yaml'


#
# Classes
#


class Configuration():

    """Configuration data object for this script"""

    k_format = 'Number Format'
    k_must_match = 'Search Term Must Match'
    k_mutex_categories = 'Mutually Exclusive Categories'
    k_regex_description = 'Regex Description'
    k_register_browsers = 'Register Browsers'
    k_search_urls = 'Search URLs'
    k_single_url = 'URL'
    k_special_keys = 'Special Select Keys'
    k_urls = 'URLs'

    def __init__(self, mapping, config_file_name=None):
        """Keep the data structure form the input file"""
        self.search_urls = mapping[self.k_search_urls]
        description = mapping.get('Description', '')
        if '{url_count_per_category}' in description:
            url_count_per_category = ''.join(
                '{0}: {1}\n'.format(category, self.get_count(category))
                for category in self.search_urls)
            description = description.format(
                url_count_per_category=url_count_per_category)
        #
        self.options = mapping.get('Options', {})
        self.translations = mapping.get('Translations', {})
        self.special_select = {}
        if not self.options.get(self.k_mutex_categories, False):
            special_select = self.options.get(self.k_special_keys, {})
            for (key, value) in special_select.items():
                if key[-2] == '-':
                    access_key = '<{0}>'.format(key)
                    self.special_select[access_key] = [
                        category for category in value['Categories']
                        if category in self.search_urls]
                    description = '{0}{1}\n'.format(
                        description,
                        self.translations.get(
                            'Special Key Selects',
                            'The key combination {0} selects {1}.').format(
                                key, value['Label']))
                #
            #
        #
        self.application = dict(
            description=description,
            title=mapping.get('Application Title', SCRIPT_NAME),
            metadata=mapping.get('Metadata', {}),
            config_file_name=config_file_name)
        self.deviant_homepages = mapping.get('Deviant Homepages', {})
        self.register_browsers()

    @classmethod
    def from_file(cls, config_file_name):
        """Read data from a configuration file"""
        return cls(configfile.read_file(config_file_name),
                   config_file_name=config_file_name)

    def get_category_search_urls(self, category):
        """Return the search URLs dict for the specified category"""
        try:
            return self.search_urls[category][self.k_urls]
        except KeyError:
            return {category: self.search_urls[category][self.k_single_url]}
        #

    def get_items(self, category):
        """Return a list of (name, url) tuples
        in the specified category
        """
        category_urls = self.get_category_search_urls(category)
        return list(category_urls.items())

    def get_list_for(self, category, search_term=None):
        """Return a list of URLs.
        If a keyword was given, return search URLs for that keyword.
        Else, return the homepages.
        """
        if search_term:
            number_format = self.search_urls[category].get(self.k_format)
            if number_format:
                search_term = format(int(search_term), number_format)
            else:
                must_match = self.search_urls[category].get(self.k_must_match)
                try:
                    match = re.match(must_match, search_term)
                except re.error as regex_error:
                    error_location = ' \u2192 '.join(
                        (self.k_search_urls, category, self.k_must_match))
                    raise ValueError(
                        self.translations.get(
                            'Regex Error',
                            'Error in regular expression\n'
                            '({0})\n'
                            'Please fix the error in the file {1}\n'
                            '({2}) and restart this program!').format(
                                regex_error,
                                self.application['config_file_name'],
                                error_location)) from regex_error
                except TypeError:
                    # No regular expression.
                    ...
                else:
                    if not match:
                        raise ValueError(
                            '{0}\n[{1}]'.format(
                                self.translations.get(
                                    'No Regex Match',
                                    'Search term {0!r} does not match'
                                    ' the regular expression {1!r}'
                                    ' and will be ignored.').format(
                                        search_term, must_match),
                                self.search_urls[category].get(
                                    self.k_regex_description,
                                    '(missing description)')))
                    #
                #
            #
            quoted_search_term = urllib.parse.quote_plus(search_term)
        else:
            quoted_search_term = None
        #
        urls_list = []
        for (name, url) in self.get_items(category):
            if quoted_search_term:
                url = url.format(search_term=quoted_search_term)
            else:
                try:
                    url = self.deviant_homepages[name]
                except KeyError:
                    # derive the homepage from the search URL
                    url_parts = urllib.parse.urlsplit(url)
                    url = urllib.parse.urlunsplit(url_parts[:2] + 3 * ('',))
                #
            #
            urls_list.append(url)
        #
        return urls_list

    def get_count(self, category):
        """Return the count of URLs per category"""
        return len(self.get_items(category))

    def register_browsers(self):
        """Register browsers defined in the config file
        if the name ist not yet occupied
        and if the path is really a file
        """
        try:
            browser_items = self.options[self.k_register_browsers].items()
        except (AttributeError, KeyError):
            return
        #
        for (name, executable_path) in browser_items:
            try:
                webbrowser.get(name)
            except webbrowser.Error:
                if os.path.isfile(executable_path):
                    webbrowser.register(
                        name,
                        None,
                        webbrowser.BackgroundBrowser(executable_path))
                #
            #
        #


class ModalDialog(tkinter.Toplevel):

    """Adapted from
    <https://effbot.org/tkinterbook/tkinter-dialog-windows.htm>
    """

    def __init__(self,
                 parent,
                 content,
                 title=None,
                 cancel_button=True):
        """Create the toplevel window and wait until the dialog is closed"""
        super().__init__(parent)
        self.transient(parent)
        if title:
            self.title(title)
        #
        self.parent = parent
        self.initial_focus = self
        self.body = tkinter.Frame(self)
        self.create_content(content)
        self.body.grid(padx=5, pady=5, sticky=tkinter.E + tkinter.W)
        self.create_buttonbox(cancel_button=cancel_button)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.action_cancel)
        self.initial_focus.focus_set()
        self.wait_window(self)

    def create_content(self, content):
        """Add content to body"""
        raise NotImplementedError

    def create_buttonbox(self, cancel_button=True):
        """Add standard button box."""
        box = tkinter.Frame(self)
        button = tkinter.Button(
            box,
            text="OK",
            width=10,
            command=self.action_ok,
            default=tkinter.ACTIVE)
        button.grid(padx=5, pady=5, row=0, column=0, sticky=tkinter.W)
        if cancel_button:
            button = tkinter.Button(
                box,
                text="Cancel",
                width=10,
                command=self.action_cancel)
            button.grid(padx=5, pady=5, row=0, column=1, sticky=tkinter.E)
        #
        self.bind("<Return>", self.action_ok)
        box.grid(padx=5, pady=5, sticky=tkinter.E + tkinter.W)

    #
    # standard button semantics

    def action_ok(self, event=None):
        """Clean up"""
        del event
        self.withdraw()
        self.update_idletasks()
        self.action_cancel()

    def action_cancel(self, event=None):
        """Put focus back to the parent window"""
        del event
        self.parent.focus_set()
        self.destroy()


class InfoDialog(ModalDialog):

    """Info dialog,
    instantiated with a seriess of (heading, paragraph) tuples
    after the parent window
    """

    def __init__(self,
                 parent,
                 *content,
                 title=None):
        """..."""
        super().__init__(parent, content, title=title, cancel_button=False)

    def create_content(self, content):
        """Add content to body"""
        for (heading, paragraph) in content:
            heading_area = tkinter.Label(
                self.body,
                text=heading,
                font=(None, 11, 'bold'),
                justify=tkinter.LEFT)
            heading_area.grid(sticky=tkinter.W, padx=5, pady=10)
            text_area = tkinter.Label(
                self.body,
                text=paragraph,
                justify=tkinter.LEFT)
            text_area.grid(sticky=tkinter.W, padx=5, pady=5)
        #


class UserInterface():

    """GUI using tkinter"""

    def __init__(self, config_file_name):
        """Initialize the url config and build the GUI"""
        self.main_window = tkinter.Tk()
        self.config = self.__config_from_file(config_file_name)
        self.main_window.title(self.config.application['title'])
        description_text = '\n'.join(
            '\n'.join(textwrap.wrap(paragraph, width=80)) for paragraph
            in self.config.application['description'].splitlines())
        description_frame = tkinter.Frame(
            self.main_window,
            borderwidth=2,
            padx=5,
            pady=5,
            relief=tkinter.GROOVE)
        description = tkinter.Label(
            description_frame,
            text=description_text,
            justify=tkinter.LEFT)
        description.grid(sticky=tkinter.W)
        description_frame.grid(
            padx=4,
            pady=2,
            sticky=tkinter.E + tkinter.W)
        #
        self.search_term_entry = None
        self.categories = {}
        self.selectors = {}
        self.selected_category = tkinter.StringVar()
        self.use_radiobuttons = self.config.options.get(
            self.config.k_mutex_categories,
            False)
        self.__build_action_frame()
        for (access_key, action) in (
                ('<Control-d>', self.clear_search_term),
                ('<Control-x>', self.cut_search_term),
                ('<Return>', self.open_urls),
                ('<Escape>', self.quit)):
            if access_key not in self.config.special_select:
                self.main_window.bind_all(access_key, action)
            #
        #
        self.search_term_entry.focus_set()
        self.main_window.mainloop()

    def __config_from_file(self, config_file_name):
        """Return a Configuration() instance from the file."""
        supported_file_types = []
        for (file_type, extensions) in configfile.SUPPORTED_FILE_TYPES.items():
            for file_extension in extensions:
                supported_file_types.append((file_type, file_extension))
            #
        #
        while True:
            if config_file_name:
                try:
                    return Configuration.from_file(config_file_name)
                except configfile.FiletypeNotSupported as error:
                    messagebox.showerror(
                        'Unsupported file type',
                        str(error),
                        icon=messagebox.ERROR)
                except configfile.InvalidFormatError as error:
                    messagebox.showerror(
                        'Invalid file format',
                        str(error),
                        icon=messagebox.ERROR)
                #
            #
            config_file_name = filedialog.askopenfilename(
                title='Select configuration file',
                parent=self.main_window,
                filetypes=supported_file_types,
                initialdir=os.path.dirname(sys.argv[0]))
            if not config_file_name:
                self.quit()
                sys.exit(0)
            #
        #

    def __build_action_frame(self):
        """Build the action frame
        with the category selector checkbuttons or radiobuttons,
        depending on the setting of the "Mutually Exclusive Categories" option.
        Return the number of lines
        """
        action_frame = tkinter.Frame(
            self.main_window,
            borderwidth=2,
            relief=tkinter.GROOVE)
        search_term_label = tkinter.Label(
            action_frame,
            text='{0}:'.format(
                self.translated('Search Term')))
        search_term_label.grid(row=0, column=0, sticky=tkinter.W)
        self.search_term_entry = tkinter.Entry(
            action_frame,
            width=50)
        self.search_term_entry.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky=tkinter.W,
            padx=5,
            pady=5)
        button = tkinter.Button(
            action_frame,
            text=self.translated(
                'Clear Button',
                default='Clear'),
            command=self.clear_search_term)
        button.grid(
            row=0,
            column=3,
            sticky=tkinter.W)
        current_grid_row = 1
        for current_category, settings in self.config.search_urls.items():
            preferred_browser = settings.get('Preferred Browser')
            category_label = current_category
            if preferred_browser:
                try:
                    webbrowser.get(preferred_browser)
                except webbrowser.Error:
                    ...
                else:
                    category_label = self.translated(
                        'Opened In',
                        default='{0} (opened in {1})').format(
                            current_category, preferred_browser.title())
                #            #
            if current_grid_row <= 12:
                access_key = '<KeyPress-F{0}>'.format(current_grid_row)
                category_label = '{0} <F{1}>'.format(category_label,
                                                     current_grid_row)
            else:
                access_key = None
            #
            if self.use_radiobuttons:
                self.selectors[current_category] = tkinter.Radiobutton(
                    action_frame,
                    text=category_label,
                    justify=tkinter.LEFT,
                    value=current_category,
                    variable=self.selected_category)
                if current_grid_row == 1:
                    self.selectors[current_category].select()
                #
            else:
                self.categories[current_category] = tkinter.IntVar()
                self.selectors[current_category] = tkinter.Checkbutton(
                    action_frame,
                    text=category_label,
                    justify=tkinter.LEFT,
                    variable=self.categories[current_category])
            #
            self.selectors[current_category].grid(
                row=current_grid_row,
                column=0,
                columnspan=2,
                sticky=tkinter.W)
            if self.config.get_count(current_category) > 1:
                def show_list_handler(self=self, category=current_category):
                    """Internal function definition to process the category
                    in the "real" handler function self.show_urls_in(),
                    compare <https://tkdocs.com/shipman/extra-args.html>.
                    """
                    return self.show_urls_in(category)
                #
                button = tkinter.Button(
                    action_frame,
                    text=self.translated('List URLs'),
                    command=show_list_handler)
                button.grid(
                    row=current_grid_row,
                    column=2,
                    sticky=tkinter.W)
            else:
                def copy_url_handler(self=self, category=current_category):
                    """Internal function definition to process the category
                    in the "real" handler function self.copy_url(),
                    compare <https://tkdocs.com/shipman/extra-args.html>.
                    """
                    return self.copy_url(category)
                #
                button = tkinter.Button(
                    action_frame,
                    text=self.translated('Copy URL'),
                    command=copy_url_handler)
                button.grid(
                    row=current_grid_row,
                    column=2,
                    sticky=tkinter.W)
            #
            current_grid_row += 1
            if access_key:
                def handler(event, self=self, category=current_category):
                    """Internal function definition to process the category
                    in the "real" handler function self.__toggle_checkbox(),
                    compare <https://tkdocs.com/shipman/extra-args.html>.
                    """
                    del event
                    return self.__toggle_selector(category)
                #
                self.main_window.bind_all(access_key, handler)
            #
        #
        button = tkinter.Button(
            action_frame,
            text=self.translated('Open Button', default='Open'),
            command=self.open_urls,
            default=tkinter.ACTIVE)
        button.grid(
            row=current_grid_row,
            column=0,
            sticky=tkinter.W,
            padx=5,
            pady=5)
        button = tkinter.Button(
            action_frame,
            text=self.translated('About Button', default='About…'),
            command=self.show_about)
        button.grid(
            row=current_grid_row,
            column=1,
            sticky=tkinter.W,
            padx=5,
            pady=5)
        button = tkinter.Button(
            action_frame,
            text=self.translated('Quit Button', default='Quit'),
            command=self.quit)
        button.grid(
            row=current_grid_row,
            column=3,
            sticky=tkinter.E,
            padx=5,
            pady=5)
        #
        action_frame.grid(
            padx=4,
            pady=2,
            sticky=tkinter.E + tkinter.W)
        #
        for special_select_key in self.config.special_select:
            def special_handler(event, self=self, key=special_select_key):
                """Internal function definition to process the key name
                in the "real" handler function self.__select_categories(),
                compare <https://tkdocs.com/shipman/extra-args.html>.
                """
                del event
                return self.__select_categories(key)
            #
            self.main_window.bind_all(special_select_key, special_handler)
        #

    def __toggle_selector(self, category):
        """Toggle a checkbox or activate a radiobutton"""
        try:
            self.selectors[category].toggle()
        except AttributeError:
            self.selectors[category].invoke()
        #

    def __select_categories(self, special_select_key):
        """Select all categories defined in the config for the
        special select key
        """
        for category in self.config.special_select.get(
                special_select_key, []):
            self.categories[category].set(1)
        #

    def translated(self, term, default=None):
        """Return the conigured translation for term,
        or default if it is not found, or term itself
        if no defaut was set
        """
        try:
            return self.config.translations[term]
        except KeyError:
            if default is None:
                return term
            #
            return default
        #

    def show_about(self):
        """Show information about the application and the source file
        in a modal dialog
        """
        try:
            with open(os.path.join(os.path.dirname(sys.argv[0]), LICENSE),
                      mode='rt',
                      encoding='utf-8') as license_file:
                license_text = license_file.read()
        except IOError:
            license_text = '(License file is missing)'
        #
        metadata = '\n'.join(
            '{0}: {1}'.format(key, value) for (key, value)
            in self.config.application['metadata'].items())
        InfoDialog(
            self.main_window,
            (self.translated('Program'),
             '{0} {1} ({2})\n\n{3}'.format(
                SCRIPT_NAME, VERSION, HOMEPAGE, license_text)),
            (self.translated('Config File'),
             '{0}\n{1}'.format(self.config.application['config_file_name'],
                               metadata)),
            title=self.translated('About Button', default='About…'))
        #

    def show_urls_in(self, category):
        """Show all URL names of the selected category in a modal dialog"""
        url_names = [name for (name, url)
                     in self.config.get_items(category)]
        InfoDialog(
            self.main_window,
            (category, '\n'.join(url_names)),
            title=self.translated('List URLs'))
        #

    def copy_url(self, category):
        """Copy the URL from the current text into the clipboard"""
        search_term = self.search_term_entry.get().strip()
        try:
            urls_list = self.config.get_list_for(
                category, search_term=search_term)
        except ValueError as value_error:
            messagebox.showerror(
                self.translated(
                    'Category Error',
                    default='Error for category {0!r}').format(category),
                str(value_error),
                icon=messagebox.ERROR)
        else:
            if len(urls_list) == 1:
                self.main_window.clipboard_clear()
                self.main_window.clipboard_append(urls_list[0])
            #
        #

    def clear_search_term(self, event=None):
        """clear the search term entry"""
        del event
        self.search_term_entry.delete(0, tkinter.END)

    def cut_search_term(self, event=None):
        """Cut out the search term: copy it to the clipboard
        and clear the entry
        """
        del event
        search_term = self.search_term_entry.get().strip()
        if search_term:
            self.main_window.clipboard_clear()
            self.main_window.clipboard_append(search_term)
            self.clear_search_term()
        #

    def open_urls(self, event=None):
        """Open the URLs with the search keywords"""
        del event
        search_term = self.search_term_entry.get().strip()
        if self.use_radiobuttons:
            selected_categories = [self.selected_category.get()]
        else:
            selected_categories = [category for category
                                   in self.config.search_urls
                                   if self.categories[category].get()]
        #
        for current_category in selected_categories:
            try:
                urls_list = self.config.get_list_for(
                    current_category, search_term=search_term)
            except ValueError as value_error:
                messagebox.showerror(
                    self.translated(
                        'Category Error',
                        default='Error for category {0!r}').format(
                            current_category),
                    str(value_error),
                    icon=messagebox.ERROR)
                continue
            #
            # Get a runnable browser instance – either the specified preferred
            # browser (if installed) or the default.
            try:
                current_browser = webbrowser.get(
                    self.config.search_urls[current_category].get(
                        'Preferred Browser'))
            except (webbrowser.Error, TypeError):
                current_browser = webbrowser.get()
            #
            try:
                current_browser.open_new(urls_list[0])
            except IndexError:
                continue
            #
            if len(urls_list) > 1:
                time.sleep(2)
                for current_url in urls_list[1:]:
                    current_browser.open_new_tab(current_url)
                #
            #
            time.sleep(2)
        #

    def quit(self, event=None):
        """Exit the application"""
        del event
        self.main_window.destroy()


#
# Functions
#


def main():
    """Main script function"""
    try:
        config_file_name = sys.argv[1]
    except IndexError:
        config_file_name = None
    #
    UserInterface(config_file_name)


if __name__ == '__main__':
    sys.exit(main())


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
