from pprint import pprint

from cloudmesh_client.keys.SSHKeyManager import SSHkey
from cloudmesh_client.db.model import KEY
from cloudmesh_base.util import path_expand
from cloudmesh_base.menu import menu_return_num

import CloudmeshDatabase


class SSHKeyDBManager(object):
    def __init__(self, cm_user=None):
        self.db = CloudmeshDatabase.CloudmeshDatabase(cm_user)

    def add(self, key_path, keyname=None, cm_user=None, source=None, uri=None):
        """
        Adds the key to the database based on the path

        :param keyname: name of the key or path to the key
        :return:
        """

        sshkey = SSHkey(path_expand(key_path))

        self.add_from_sshkey(sshkey.__key__, keyname, cm_user, source=source, uri=uri)

    def add_from_dict(self, d):
        pprint(d)

        keyname = d['keyname']
        key_obj = KEY(name=keyname,
                      label=keyname,
                      cloud="general",
                      cm_user=d['cm_user']
                      )

        key_obj.name = d['keyname']
        key_obj.uri = d['uri']
        key_obj.source = d['source']
        key_obj.comment = d['comment']
        key_obj.value = d['string'] + " " + d['comment']
        key_obj.fingerprint = d['fingerprint']

        # pprint (key_obj.__dict__)
        self.db.add([key_obj])
        self.db.save()

    def add_from_sshkey(self, sshkey, keyname=None, cm_user=None, source=None, uri=None):

        if keyname is None:
            try:
                keyname = sshkey['name']
            except:
                pass
        if keyname is None:
            print ("ERROR: keyname is none")

        key_obj = KEY(name=keyname,
                      label=keyname,
                      cloud="general",
                      cm_user=cm_user
                      )

        key_obj.name = keyname
        key_obj.uri = uri
        key_obj.source = source
        key_obj.comment = sshkey['comment']
        key_obj.value = sshkey['string']
        key_obj.fingerprint = sshkey['fingerprint']

        pprint(key_obj.__dict__)
        self.db.add([key_obj])
        self.db.save()

    def delete(self, keyname):
        """
        Deletes the key from the database based on the keyname

        :param keyname: name of the key to be delete
        :return:
        """
        self.db.delete_by_name(KEY, name=keyname)

    def set_default(self, keyname):
        if self.get_default():
            self.get_default().default = 'False'
        self.find(keyname).default = 'True'
        self.db.save()

    def get_default(self):
        value = "True"
        return self.db.find(KEY, default=value)

    def find(self, keyname):
        """
        Finds the key on the database based on the keyname

        :param keyname: name of the key to be found
        :return: Query object of the search
        """
        return self.db.find_by_name(KEY, keyname)

    def find_all(self):
        """

        :return: Query object from all the entries
        """
        return self.db.find(KEY).all()

    def table_dict(self):
        """

        :return: dict from all elements in the table KEY
        """
        return self.db.dict(KEY)

    def update(self, clouds):
        # i'm not sure how this function works
        self.db.update("key", clouds)

    def delete_all(self):
        """
        Deletes all the entries from KEY table

        :return:
        """
        self.db.delete_all(['KEY'])

    def select(self):
        options = []
        d = self.dict()
        for i in d:
            print ('i:', i)
            line = '{}: {}'.format(d[i]['name'], d[i]['fingerprint'])
            options.append(line)
        num = menu_return_num('KEYS', options)
        if num != 'q':
            return options[num - 1]
        return num

    def object_to_dict(self, obj):
        """

        :param obj: object to be converted to dict
        :return: dict from the object
        """
        return self.db.object_to_dict(obj)
