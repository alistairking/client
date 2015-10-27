from __future__ import print_function
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default


class FlavorCommand(object):
    topics = {"flavor": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command flavor")

    @command
    def do_flavor(self, args, arguments):
        """
        ::

            Usage:
                flavor refresh [--cloud=CLOUD]
                flavor list [--cloud=CLOUD] [--format=FORMAT]
                flavor show ID [--cloud=CLOUD] [--refresh] [--format=FORMAT]

                This lists out the flavors present for a cloud

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --refresh        refreshes the data before displaying it
                                from the cloud

            Examples:
                cm flavor refresh
                cm flavor list
                cm flavor list --format=csv
                cm flavor show 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh

        """
        try:
            cloud = arguments["--cloud"] or Default.get("cloud")
        except:
            Console.error("xxx Default cloud doesn't exist")

        if arguments["refresh"]:

            if not cloud:
                Console.error("Default cloud doesn't exist")
                return

            msg = "Refresh flavor for cloud {:}.".format(cloud)
            if Flavor.refresh(cloud):
                Console.ok("{:} ok".format(msg))
            else:
                Console.error(msg)
            return

        if arguments["list"]:
            if not cloud:
                Console.error("Default cloud doesn't exist")
                return
            output_format = arguments["--format"]
            result = Flavor.list(cloud, output_format)
            if result is None:
                Console.error("No flavors found, please use 'cm flavor "
                              "refresh'")
            else:
                print(result)

        if arguments["show"]:
            id = arguments['ID']
            output_format = arguments["--format"]
            live = arguments['--refresh']
            if not cloud:
                Console.error("Default cloud doesn't exist")
                return
            result = Flavor.details(cloud, id, live, output_format)
            print(result)
            return

