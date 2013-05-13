from ioc.extra.command import Command

class ListTypeCommand(Command):
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def initialize(self, parser):
        parser.description = "List node types available"

    def execute(self, args, output):
        output.write("Nodes type available:\n")

        for name, service in self.node_manager.handlers.iteritems():
            output.write(" - %s \n" % name)

        output.write("\n--\nPython Element - Thomas Rabaix <thomas.rabaix@gmail.com>\n")