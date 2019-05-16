# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This file contains routines to verify the correctness of UCD strings.
"""


# STDLIB
import re

# LOCAL
from astropy.utils import data
from astropy.table import Table
from astropy.votable.tree import Field

__all__ = ['parse_ucd', 'check_ucd']


class UCDWords:
    """
    Manages a list of acceptable UCD words.

    Works by reading in a data file exactly as provided by IVOA.  This
    file resides in data/ucd1p-words.txt.
    """

    def __init__(self):
        self._primary = set()
        self._secondary = set()
        self._descriptions = {}
        self._capitalization = {}

        with data.get_pkg_data_fileobj(
                "data/ucd1p-words.txt", encoding='ascii') as fd:
            for line in fd.readlines():
                type, name, descr = [
                    x.strip() for x in line.split('|')]
                name_lower = name.lower()
                if type in 'QPEV':
                    self._primary.add(name_lower)
                if type in 'QSEV':
                    self._secondary.add(name_lower)
                self._descriptions[name_lower] = descr
                self._capitalization[name_lower] = name

    def is_primary(self, name):
        """
        Returns True if *name* is a valid primary name.
        """
        return name.lower() in self._primary

    def is_secondary(self, name):
        """
        Returns True if *name* is a valid secondary name.
        """
        return name.lower() in self._secondary

    def get_description(self, name):
        """
        Returns the official English description of the given UCD
        *name*.
        """
        return self._descriptions[name.lower()]

    def normalize_capitalization(self, name):
        """
        Returns the standard capitalization form of the given name.
        """
        return self._capitalization[name.lower()]


_ucd_singleton = None


def parse_ucd(ucd, check_controlled_vocabulary=False, has_colon=False):
    """
    Parse the UCD into its component parts.

    Parameters
    ----------
    ucd : str
        The UCD string

    check_controlled_vocabulary : bool, optional
        If `True`, then each word in the UCD will be verified against
        the UCD1+ controlled vocabulary, (as required by the VOTable
        specification version 1.2), otherwise not.

    has_colon : bool, optional
        If `True`, the UCD may contain a colon (as defined in earlier
        versions of the standard).

    Returns
    -------
    parts : list
        The result is a list of tuples of the form:

            (*namespace*, *word*)

        If no namespace was explicitly specified, *namespace* will be
        returned as ``'ivoa'`` (i.e., the default namespace).

    Raises
    ------
    ValueError : *ucd* is invalid
    """
    global _ucd_singleton
    if _ucd_singleton is None:
        _ucd_singleton = UCDWords()

    if has_colon:
        m = re.search(r'[^A-Za-z0-9_.:;\-]', ucd)
    else:
        m = re.search(r'[^A-Za-z0-9_.;\-]', ucd)
    if m is not None:
        raise ValueError("UCD has invalid character '{}' in '{}'".format(
                m.group(0), ucd))

    word_component_re = r'[A-Za-z0-9][A-Za-z0-9\-_]*'
    word_re = r'{}(\.{})*'.format(word_component_re, word_component_re)

    parts = ucd.split(';')
    words = []
    for i, word in enumerate(parts):
        colon_count = word.count(':')
        if colon_count == 1:
            ns, word = word.split(':', 1)
            if not re.match(word_component_re, ns):
                raise ValueError("Invalid namespace '{}'".format(ns))
            ns = ns.lower()
        elif colon_count > 1:
            raise ValueError("Too many colons in '{}'".format(word))
        else:
            ns = 'ivoa'

        if not re.match(word_re, word):
            raise ValueError("Invalid word '{}'".format(word))

        if ns == 'ivoa' and check_controlled_vocabulary:
            if i == 0:
                if not _ucd_singleton.is_primary(word):
                    if _ucd_singleton.is_secondary(word):
                        raise ValueError(
                            "Secondary word '{}' is not valid as a primary "
                            "word".format(word))
                    else:
                        raise ValueError("Unknown word '{}'".format(word))
            else:
                if not _ucd_singleton.is_secondary(word):
                    if _ucd_singleton.is_primary(word):
                        raise ValueError(
                            "Primary word '{}' is not valid as a secondary "
                            "word".format(word))
                    else:
                        raise ValueError("Unknown word '{}'".format(word))

        try:
            normalized_word = _ucd_singleton.normalize_capitalization(word)
        except KeyError:
            normalized_word = word
        words.append((ns, normalized_word))

    return words


def check_ucd(ucd, check_controlled_vocabulary=False, has_colon=False):
    """
    Returns False if *ucd* is not a valid `unified content descriptor`_.

    Parameters
    ----------
    ucd : str
        The UCD string

    check_controlled_vocabulary : bool, optional
        If `True`, then each word in the UCD will be verified against
        the UCD1+ controlled vocabulary, (as required by the VOTable
        specification version 1.2), otherwise not.

    has_colon : bool, optional
        If `True`, the UCD may contain a colon (as defined in earlier
        versions of the standard).

    Returns
    -------
    valid : bool
    """
    if ucd is None:
        return True

    try:
        parse_ucd(ucd,
                  check_controlled_vocabulary=check_controlled_vocabulary,
                  has_colon=has_colon)
    except ValueError:
        return False
    return True


def find_columns_by_ucd(table, ucd):
    """
    Given an astropy table derived from a VOTABLE, this function returns
    the first Column object that has the given Universal Content Descriptor (UCD).
    The name field of the returned value contains the column name and can be used
    for accessing the values in the column.

    Parameters
    ----------
    table : VOTable or astropy.table.Table
        The votable or astropy table derived from a VOTable to search through
        for all the columns with a particular UCD.
    ucd : str
        The UCD identifying the column to be found.

    Returns
    -------
    colnames : list of str
        The list of names of the columns that has the UCD named ``ucd``. If
        ``table`` is a VOTable, this name is the ID unless there's no ID in
        which case it's the name.
    """
    colnames = []
    if isinstance(table, Table):
        for col in table.columns:
            ucdval = col.meta.get('ucd')
            if ucdval is not None and ucd in ucdval:
                colnames.append(col.name)
    else:
        # assume it's a VOTable
        for elem in table.iter_fields_and_params():
            if isinstance(elem, Field):
                ucdval = elem.ucd
                if ucdval is not None and ucd in ucdval:
                    colnames.append(elem.name if elem.ID is None else elem.ID)  # THIS MIGHT BE A BAD IDEA!

    return colnames
