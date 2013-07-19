# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def unicode_sorter(input):
    """ This function implements sort keys for the german language according to
    DIN 5007."""

    # key1: compare words lowercase and replace umlauts according to DIN 5007
    key1=input.lower()
    key1=key1.replace(u"ä", u"a")
    key1=key1.replace(u"ö", u"o")
    key1=key1.replace(u"ü", u"u")
    key1=key1.replace(u"ß", u"ss")

    # key2: sort the lowercase word before the uppercase word and sort
    # the word with umlaut after the word without umlaut
    # key2=input.swapcase()

    # in case two words are the same according to key1, sort the words
    # according to key2.
    return key1
