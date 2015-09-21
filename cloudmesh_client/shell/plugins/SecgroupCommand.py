from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.secgroup import SecGroup

class SecgroupCommand(object):

    topics = {"secgroup": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command secgroup")

    @command
    def do_secgroup(self, args, arguments):
        """
        ::

            Usage:
                secgroup list CLOUD TENANT
                secgroup create CLOUD TENANT LABEL
                secgroup delete CLOUD TENANT LABEL
                secgroup rules-list CLOUD TENANT LABEL
                secgroup rules-add CLOUD TENANT LABEL FROMPORT TOPORT PROTOCOL CIDR
                secgroup rules-delete CLOUD TENANT LABEL FROMPORT TOPORT PROTOCOL CIDR
                secgroup -h | --help
                secgroup --version

            Options:
                -h            help message

            Arguments:
                CLOUD         Name of the IaaS cloud e.g. india_openstack_grizzly.
                TENANT        Name of the tenant, e.g. fg82.
                LABEL         The label/name of the security group
                FROMPORT      Staring port of the rule, e.g. 22
                TOPORT        Ending port of the rule, e.g. 22
                PROTOCOL      Protocol applied, e.g. TCP,UDP,ICMP
                CIDR          IP address range in CIDR format, e.g., 129.79.0.0/16

            Description:
                security_group command provides list/add/delete
                security_groups for a tenant of a cloud, as well as
                list/add/delete of rules for a security group from a
                specified cloud and tenant.


            Examples:
                $ secgroup list india fg82
                $ secgroup rules-list india fg82 default
                $ secgroup create india fg82 webservice
                $ secgroup rules-add india fg82 webservice 8080 8088 TCP "129.79.0.0/16"

        """
        # pprint(arguments)

        if arguments["list"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            result = SecGroup.list_secgroup(tenant,cloud)

            if result:
                print(result)
            else:
                Console.error("No Security Groups found in the cloudmesh database!")
            return

        elif arguments["create"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]

            # Create returns uuid of created sec-group
            uuid = SecGroup.create(label, cloud, tenant)

            if uuid:
                Console.ok("Created a new security group [{}] with UUID [{}]"
                       .format(label, uuid))
            else:
                Console.error("Security group [{}], for cloud [{}], & tenant [{}] already exists!"
                              .format(label, cloud, tenant))
            return

        elif arguments["delete"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]

            result = SecGroup.delete_secgroup(label, cloud, tenant)
            if result:
                print(result)
            else:
                Console.error("Security Group [{}, {}, {}] could not be deleted"
                              .format(label, cloud, tenant))

            return

        elif arguments["rules-delete"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]
            from_port = arguments["FROMPORT"]
            to_port = arguments["TOPORT"]
            protocol = arguments["PROTOCOL"]
            cidr = arguments["CIDR"]

            # Get the security group
            sec_group = SecGroup.get_secgroup(label, tenant, cloud)
            if sec_group:
                # Get the rules
                result = SecGroup.delete_rule(sec_group, from_port, to_port, protocol, cidr)
                if result:
                    print(result)
                else:
                    Console.error("Rule [{} | {} | {} | {}] could not be deleted"\
                        .format(from_port, to_port, protocol, cidr))

            return

        elif arguments["rules-list"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]

            # Get the security group
            sec_group = SecGroup.get_secgroup(label, tenant, cloud)
            if sec_group:
                # Get the rules
                result = SecGroup.get_rules(sec_group.uuid)
                print(result)
            else:
                Console.error("Security Group with label [{}], cloud [{}], & tenant [{}] not found!"
                              .format(label, cloud, tenant))
                return

        elif arguments["rules-add"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]
            from_port = arguments["FROMPORT"]
            to_port = arguments["TOPORT"]
            protocol = arguments["PROTOCOL"]
            cidr = arguments["CIDR"]

            # Get the security group
            sec_group = SecGroup.get_secgroup(label, tenant, cloud)
            if sec_group:
                # Add rules to the security group
                SecGroup.add_rule(sec_group, from_port, to_port, protocol, cidr)
            else:
                Console.error("Security Group with label [{}], cloud [{}], & tenant [{}] not found!"
                              .format(label, cloud, tenant))
                return

        #TODO: Add Implementation
        elif arguments["--version"]:
            Console.ok('Version: ')

if __name__ == '__main__':
    command = cm_shell_security_group()
    command.do_security_group("list")
    command.do_security_group("a=x")
    command.do_security_group("x")
