#   Copyright (c) 2015, Jeremy Schulman (nwkautomaniac@gmail.com)
#
#   This code is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, version 3 of the License.  A copy of
#   this license can be found accompanying this sofware respository.
#   You can also find a copy of the GNU General Public License
#   here: <http://www.gnu.org/licenses/gpl-3.0.html>
#
#   The author provides no warranties regarding the software, which is
#   provided "AS-IS" and your use of this software is entirely at your
#   own risk.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR DAMAGES OF ANY
#   KIND RELATING TO USE OF THE SOFTWARE, INCLUDING WITHOUT LIMITATION
#   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#   DAMAGES; ANY PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION, HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE), EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
from itertools import product

__all__ = ['bracket_expansion']

_bracket = '\[.+?\]'
_bracket_extract = '\[(-?\d+)\-(-?\d+)(,\d)?\]'


def bracket_expansion(pattern, default_step=1):
    """
    Returns a generator that will yield string-replacements of
    pattern given the bracket notation.  Bracket notation is
        [<start>-<stop>]                # step = <default_step>
        [<start>-<stop>,<step>]         # step is caller defined

    For example:
        # create 'ifs' as a generator for even numbered
        # ports on two different linecards:

        ifs = bracket_expansion('ge-[0-1]/0/[0-47,2]')

        # loop through each
        for ifname in ifs:
            print ifname

    You can also get the complete list of values by applying
    the 'list' function, for example:

        ifs = list(bracket_expansion('ge-0/0/[0-47]'))
        # ifs is now a list containing 48 entries
    """
    re_br = re.compile(_bracket)
    re_ext = re.compile(_bracket_extract)

    # extract brackets from pattern

    brackets = re_br.findall(pattern)

    # extact values from the brackets [start-stop,step]  the step
    # value is optional, and defaults to :default_step:

    range_inputs = lambda n: (int(n[0]), int(n[1])+1, default_step if not n[2] else int(n[2][1:]))
    extracts = [range_inputs(re_ext.match(b).groups()) for b in brackets]

    # create the replacement numbers for each generator value by
    # taking the product of the extracted bracket values.  the product function
    # will create an iterator, so this is all nice and memory effecient

    repls = product(*[xrange(*n) for n in extracts])

    # create generator to string-substitue the replacement value
    # into the pattern on each iteration.  the technique is to make
    # each replacement value (originally a tuple) into a list.
    # this makes it pop'able.  so (1,2) becomes [1,2] so we can pop
    # values off the fron as the re.sub function iterates through
    # the string, yo!

    for each in repls:
        nums = list(each)
        yield(re_br.sub(lambda x: str(nums.pop(0)), pattern))
