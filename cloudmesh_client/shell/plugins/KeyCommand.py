from __future__ import print_function
import json

import yaml

from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand


class KeyCommand(PluginCommand, CloudPluginCommand):

    topics = {"key": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command key")

    # noinspection PyUnusedLocal
    @command
    def do_key(self, args, arguments):
        """
        ::

           Usage:
             key  -h | --help
             key list [--source=db] [--format=FORMAT]
             key list --source=cloudmesh [--format=FORMAT]
             key list --source=ssh [--dir=DIR] [--format=FORMAT]
             key load [--format=FORMAT]
             key list --source=git [--format=FORMAT] [--username=USERNAME]
             key add --git [--name=KEYNAME] FILENAME
             key add --ssh [--name=KEYNAME]
             key add [--name=KEYNAME] FILENAME
             key get NAME
             key default [KEYNAME | --select]
             key delete (KEYNAME | --select | --all) [--force]
             key upload [KEYNAME] [--cloud=CLOUD]
             key map [--cloud=CLOUD]

           Manages the keys

           Arguments:

             SOURCE         db, ssh, all
             KEYNAME        The name of a key. For key upload it defaults to the default key name.
             FORMAT         The format of the output (table, json, yaml)
             FILENAME       The filename with full path in which the key
                            is located
             NAME_ON_CLOUD  Typically the name of the keypair on the cloud.

           Options:

              --dir=DIR                     the directory with keys [default: ~/.ssh]
              --format=FORMAT               the format of the output [default: table]
              --source=SOURCE               the source for the keys [default: db]
              --username=USERNAME           the source for the keys [default: none]
              --name=KEYNAME                The name of a key
              --all                         delete all keys
              --force                       delete the key form the cloud
              --name_on_cloud=NAME_ON_CLOUD Typically the name of the keypair on the cloud.

           Description:

           key list --source=git  [--username=USERNAME]

              lists all keys in git for the specified user. If the
              name is not specified it is read from cloudmesh.yaml

           key list --source=ssh  [--dir=DIR] [--format=FORMAT]

              lists all keys in the directory. If the directory is not
              specified the default will be ~/.ssh

           key list --source=cloudmesh  [--dir=DIR] [--format=FORMAT]

              lists all keys in cloudmesh.yaml file in the specified directory.
               dir is by default ~/.cloudmesh

           key list [--format=FORMAT]

               list the keys in teh giiven format: json, yaml,
               table. table is default

           key list

                Prints list of keys. NAME of the key can be specified

               
           key add [--name=keyname] FILENAME

               adds the key specifid by the filename to the key
               database

           key get NAME

               Retrieves the key indicated by the NAME parameter from database
               and prints its fingerprint.

           key default [NAME]

                Used to set a key from the key-list as the default key
                if NAME is given. Otherwise print the current default
                key

           key delete NAME

                deletes a key. In yaml mode it can delete only key that
                are not saved in the database

           key rename NAME NEW

                renames the key from NAME to NEW.
                
        """
        # pprint(arguments)

        def _print_dict(d, header=None, format='table'):
            if format == "json":
                return json.dumps(d, indent=4)
            elif format == "yaml":
                return yaml.dump(d, default_flow_style=False)
            elif format == "table":
                return dict_printer(d,
                                    order=["name",
                                           "comment",
                                           "uri",
                                           "fingerprint",
                                           "source"],
                                    output="table",
                                    sort_keys=True)
            else:
                return d
                # return dict_printer(d,order=['cm_id, name, fingerprint'])

        directory = Config.path_expand(arguments["--dir"])

        if arguments['list']:
            _format = arguments['--format']
            _source = arguments['--source']
            _dir = arguments['--dir']

            if arguments['--source'] == 'ssh':

                try:
                    sshm = SSHKeyManager()
                    sshm.get_from_dir(directory)
                    d = dict(sshm.__keys__)
                    print(_print_dict(d, format=_format))
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem listing keys from ssh")

            elif arguments['--source'] in ['cm', 'cloudmesh']:

                try:
                    sshm = SSHKeyManager()
                    m = sshm.get_from_yaml(load_order=directory)
                    d = dict(m.__keys__)
                    print(_print_dict(d, format=_format))
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem listing keys from `{:}`".format(arguments['--source']))

            elif arguments['--source'] in ['git']:

                username = arguments["--username"]
                # print(username)
                if username == 'none':
                    conf = ConfigDict("cloudmesh.yaml")
                    username = conf["cloudmesh.github.username"]

                sshm = SSHKeyManager()
                try:
                    sshm.get_from_git(username)
                    d = dict(sshm.__keys__)
                    print(_print_dict(d, format=_format))
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem listing git keys from database")
                    return ""

            elif arguments['--source'] == 'db':

                try:
                    sshdb = SSHKeyDBManager()
                    d = sshdb.table_dict()
                    if d != {}:
                        print(_print_dict(d, format=arguments['--format']))
                        msg = "info. OK."
                        Console.ok(msg)
                    else:
                        Console.error("No keys in the database")
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem listing keys from database")

        elif arguments['load']:
            _format = arguments['--format']
            _dir = arguments['--dir']

            try:
                sshm = SSHKeyManager()
                m = sshm.get_from_yaml(load_order=directory)
                d = dict(m.__keys__)

                sshdb = SSHKeyDBManager()

                for keyname in m.__keys__:
                    filename = m[keyname]["path"]
                    try:
                        sshdb.add(filename,
                                  keyname,
                                  source="yaml",
                                  uri="file://" + filename)
                    except Exception as e:
                        Console.error("problem adding key {}:{}".format(
                            keyname, filename))

                print(_print_dict(d, format=_format))
                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                Console.error("Problem adding keys from yaml file")

        elif arguments['get']:

            try:
                name = arguments['NAME']
                sshdb = SSHKeyDBManager()
                d = sshdb.table_dict()

                for i in d:
                    if d[i]["name"] == name:
                        key = d[i]
                        print("{:}: {:}".format(key['name'], key['fingerprint']))
                        msg = "info. OK."
                        Console.ok(msg)
                        return ""
                    else:
                        pass
                Console.error("The key is not in the database")
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print (e)
                Console.error("The key is not in the database")

        # key add --git KEYNAME
        #      key add --ssh KEYNAME
        #      key add [--path=PATH]  KEYNAME

        elif arguments['add'] and arguments["--git"]:

            print('git add')
            sshdb = SSHKeyDBManager()
            keyname = arguments['--name']
            gitkeyname = arguments['NAME']
            filename = arguments['FILENAME']

            # Are we adding to the database as well?
            # sshdb.add(filename, keyname, source="ssh", uri="file://"+filename)

            username = arguments["--username"]

            if username == 'none':
                conf = ConfigDict("cloudmesh.yaml")
                username = conf["cloudmesh.github.username"]
            print(username)

            sshm = SSHKeyManager()
            try:
                sshm.get_from_git(username)
                d = dict(sshm.__keys__)
                print(d)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print (e)
                Console.error("Problem adding keys to git for user: " + username)
                return ""

            try:
                # FIXME: correct code to add to git
                d[gitkeyname]['keyname'] = keyname
                d[gitkeyname]['user'] = None
                d[gitkeyname]['source'] = 'git'
                # sshdb.add_from_dict(d[gitkeyname])
            except Exception as e:
                Console.error("The key already exists")

        elif arguments['add'] and arguments["--ssh"]:

            # print('ssh add')
            sshdb = SSHKeyDBManager()
            keyname = arguments['--name']
            filename = Config.path_expand("~/.ssh/id_rsa.pub")
            try:
                sshdb.add(filename, keyname, source="ssh", uri="file://" + filename)
                print("Key {:} successfully added to the database".format(keyname or ""))
                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                """
                import traceback
                print(traceback.format_exc())
                print (e)
                print (keyname)
                print (filename)
                """
                Console.error("Problem adding the key `{}` from file `{}`".format(keyname, filename))

        elif arguments['add'] and not arguments["--git"]:

            # print('ssh add')
            sshdb = SSHKeyDBManager()
            keyname = arguments['--name']
            filename = arguments['FILENAME']
            try:
                sshdb.add(filename, keyname, source="ssh", uri="file://" + filename)
                print("Key {:} successfully added to the database".format(keyname or ""))
                msg = "info. OK."
                Console.ok(msg)

            except ValueError as e:
                Console.error("The key `{}` already exists".format(keyname), traceflag=False)
            """
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print (e)
                print (keyname)
                print (filename)
                Console.error("Problem adding the key `{}` from file `{}`".format(keyname, filename))
            """
            return ""

        elif arguments['default']:

            # print("default")

            if arguments['KEYNAME']:
                keyname = None
                try:
                    keyname = arguments['KEYNAME']
                    sshdb = SSHKeyDBManager()
                    sshdb.set_default(keyname)
                    Default.set_key(keyname)
                    print("Key {:} set as default".format(keyname))
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Setting default for key {:} failed.".format(keyname))

            elif arguments['--select']:
                keyname = None
                try:
                    sshdb = SSHKeyDBManager()
                    select = sshdb.select()
                    if select != 'q':
                        keyname = select.split(':')[0]
                        print("Setting key: {:} as default.".format(keyname))
                        sshdb.set_default(keyname)
                        msg = "info. OK."
                        Console.ok(msg)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Setting default for selected key {:} failed.".format(keyname))

            else:
                try:
                    sshdb = SSHKeyDBManager()
                    d = sshdb.table_dict()

                    for i in d:
                        if d[i]["is_default"] == "True":
                            key = d[i]
                            print("{:}: {:}".format(key['name'], key['fingerprint']))
                            msg = "info. OK."
                            Console.ok(msg)
                            return ""
                        else:
                            pass
                    Console.error("The key is not in the database")
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem retrieving default key.")

        elif arguments['delete']:

            delete_on_cloud = arguments["--force"] or False
            # print ("DDD", delete_on_cloud)
            if arguments['--all']:
                try:
                    sshm = SSHKeyManager(delete_on_cloud=delete_on_cloud)
                    sshm.delete_all_keys()
                    print("All keys from the database deleted successfully.")
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem deleting keys")
            elif arguments['--select']:
                keyname = None
                sshdb = SSHKeyDBManager()
                select = sshdb.select()
                if select != 'q':
                    try:
                        keyname = select.split(':')[0]
                        print("Deleting key: {:}...".format(keyname))
                        sshm = SSHKeyManager(delete_on_cloud=delete_on_cloud)
                        sshm.delete_key(keyname)
                        msg = "info. OK."
                        Console.ok(msg)
                    except Exception as e:
                        import traceback
                        print(traceback.format_exc())
                        print (e)
                        Console.error("Problem deleting the key `{:}`".format(keyname))
            else:
                keyname = None
                try:
                    keyname = arguments['KEYNAME']
                    sshm = SSHKeyManager(delete_on_cloud=delete_on_cloud)
                    sshm.delete_key(keyname)
                    print("Key {:} deleted successfully from database.".format(keyname))
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem deleting the key `{:}`".format(keyname))

        elif arguments['upload']:

            try:
                #
                # get username
                #
                conf = ConfigDict("cloudmesh.yaml")
                username = conf["cloudmesh"]["profile"]["username"]
                if username in ['None', 'TBD']:
                    username = None

                #
                # get cloudnames
                #
                clouds = []
                cloud = arguments["--cloud"] or Default.get_cloud()
                if cloud == "all":
                    config = ConfigDict("cloudmesh.yaml")
                    clouds = config["cloudmesh"]["clouds"]
                else:
                    clouds.append(cloud)

                #
                # get keyname
                #

                for cloud in clouds:
                    status = 0
                    sshdb = SSHKeyDBManager()
                    sshm = SSHKeyManager()
                    keys = sshdb.find_all()
                    for keyid in keys:
                        key = keys[keyid]

                        print ("upload key {} -> {}".format(key["name"],
                                                            cloud))

                        try:
                            status = sshm.add_key_to_cloud(
                                username,
                                key["name"],
                                cloud,
                                key["name"])

                        except Exception as e:
                            print (e)
                            if "already exists" in str(e):
                                print ("key already exists. Skipping "
                                       "upload. ok.")
                        if status == 1:
                            print("Problem uploading key. failed.")
                msg = "info. OK."
                Console.ok(msg)

            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print (e)
                Console.error("Problem adding key to cloud")

        elif arguments['map']:
            try:
                cloud = arguments["--cloud"] or Default.get_cloud()
                sshm = SSHKeyManager()
                map_dict = sshm.get_key_cloud_maps(cloud)
                print(dict_printer(map_dict,
                                   order=["user", "key_name", "cloud_name", "key_name_on_cloud"]))

            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print (e)
                Console.error("Problem adding key to cloud")
