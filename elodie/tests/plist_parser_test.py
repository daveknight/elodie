# -*- coding: utf-8
# Project imports
import os
import shutil
import sys

from nose.tools import raises
from xml.parsers.expat import ExpatError

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))))
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import helper
from elodie.plist_parser import Plist


def test_init_with_valid_plist_file():
    plist = Plist(helper.get_file('plist.plist'))
    assert plist is not None

@raises(ExpatError)
def test_init_with_invalid_plist_file():
    plist = Plist(helper.get_file('plist-invalid.plist'))
    assert plist is not None

@raises(IOError)
def test_init_with_nonexistant_plist_file():
    plist = Plist('does-not-exist')

def test_update_and_write_plist():
    temporary_folder, folder = helper.create_working_folder()

    plist_file = helper.get_file('plist.plist')
    origin = '%s/plist.plist' % folder
    destination = '%s/destination.plist' % folder

    shutil.copyfile(plist_file, origin)

    plist = Plist(origin)
    plist.update_key('common/title', 'this is a new title')
    plist.write_file(destination)

    with open(origin, 'r') as f_origin:
        origin_contents = f_origin.read()

    with open(destination, 'r') as f_destination:
        destination_contents = f_destination.read()

    assert origin_contents != destination_contents, destination_contents
    assert 'this is a new title' not in origin_contents, origin_contents
    assert 'this is a new title' in destination_contents, destination_contents
