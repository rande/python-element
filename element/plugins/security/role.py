#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy

class RoleHierarchy(object):
    def __init__(self, hierarchie=None):
        self.roles = {}
        if hierarchie:
            self.roles = self.buildRoles(copy.deepcopy(hierarchie))

    def get_reachable_roles(self, roles):
        reachable_roles = []

        for role in roles:
            if role in self.roles:
                reachable_roles += self.roles[role]

        return list(set(reachable_roles))

    def buildRoles(self, hierarchie):
        roles = {}

        # print ""
        for main_role, main_roles in hierarchie.iteritems():
            # print main_role, main_roles
            elements = main_roles[:]
            roles[main_role] = main_roles[:] + [main_role]

            parsed = []

            while len(elements) != 0:
                role = elements.pop()

                if role in parsed:
                    continue

                parsed.append(role)

                if role not in hierarchie:
                    continue

                roles[main_role] += hierarchie[role]
                roles[main_role] = list(set(roles[main_role])) # unique ...

                elements = roles[main_role][:]

        return roles