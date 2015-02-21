#   Author: Jeremy Schulman (nwkautomaniac@gmail.com)
#
#   This code is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.
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

from nwkautomaniac.ezcfmaker import EzCFMaker

ez_csv = EzCFMaker.CSV(datafile='hosts_data.csv', template='cisco.j2')


## ---------------------------------------------------------------------------
## add a transform function that will take all the "vlan_" fields and
## create a new 'vlans' dictionary based on the desired algorithm
## ---------------------------------------------------------------------------

@ez_csv.transform
def vlan_data(row):
    # the first thing we want to do is remove all fields that start with
    # "vlan_" from the original dictionary.  we only want to keep the
    # fields that do not have a value of "0" as the csv-data uses "0" to
    # indicate a non-used vlan.  The result is a dictionary.

    vlan_fields = {
        field_name: field_value
        for field_name, field_value in row.items()
        if field_name.startswith('vlan_') and row.pop(field_name)
        if field_value != '0'
    }

    # now that we have that field list, we want to map the "vlan_name_<n>"
    # values to the actual "vlan_id_<n>" values.  we want to create a new
    # entry in the original dictionary called 'vlans' to store this new
    # vlan dictionary.  We also need to handle the case when the vlan name
    # has whitespace; so covert spaces to underscoores (_).

    row['vlans'] = {
        vlan_fields[f].replace(' ', '_'): vlan_fields[f.replace('name', 'id')]
        for f in vlan_fields if f.startswith('vlan_name')
    }

## ---------------------------------------------------------------------------
## now make all the per-host configuration files
## ---------------------------------------------------------------------------

ez_csv.make()
