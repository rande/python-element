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