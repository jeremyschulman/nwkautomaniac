#   Author: Jeremy Schulman (nwkautomaniac@gmail.com)
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

import os
import jinja2
import csv

__all__ = ['EzCFMaker']


class EzCFMaker_CSV(object):
    def __init__(self, j2env=None, templatedirs=None, datafile=None, template=None):
        self._jenv = j2env or self._init_j2(templatedirs)
        self._transformers = []
        self.host_filename = self._default_host_filename

        if datafile: self.datafile = datafile
        if template: self.template = template

    def _init_j2(self, templatedirs=None):
        ldr = jinja2.FileSystemLoader(templatedirs or os.getcwd())
        return jinja2.Environment(loader=ldr, trim_blocks=True, lstrip_blocks=True)

    ##### --------------------------------------------------------------------
    #####               PUBLIC METHODS
    ##### --------------------------------------------------------------------

    def make(self):
        for row in self._csv_d:
            for txf in self._transformers: txf(row)
            with open(self._host_filename(row), 'w+') as f:
                f.write(self._template.render(row))

    ##### --------------------------------------------------------------------
    #####               PROPERTIES
    ##### --------------------------------------------------------------------

    @property
    def datafile(self):
        return self._csv_filename

    @datafile.setter
    def datafile(self, value):
        self._csv_filename = value
        self._csv_f = open(self._csv_filename)
        self._csv_d = csv.DictReader(self._csv_f)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template_filename = value
        self._template = self._jenv.get_template(value)

    @property
    def host_filename(self):
        return self._host_filename

    @host_filename.setter
    def host_filename(self, value):
        self._host_filename = value

    ##### --------------------------------------------------------------------
    #####               DECORATORS
    ##### --------------------------------------------------------------------

    def transform(self, func):
        self._transformers.append(func)

    ##### --------------------------------------------------------------------
    #####               PRIVATE METHODS
    ##### --------------------------------------------------------------------

    def _default_host_filename(self, row):
        return row['hostname'] + '.txt'


class EzCFMaker(object):
    CSV = EzCFMaker_CSV
