""" run with

python setup.py install; nosetests -v --nocapture  tests/test_default.py:Test_default.test_001

nosetests -v --nocapture tests/test_default.py

or

nosetests -v tests/test_vm.py

"""
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING
import os
from time import sleep
from cloudmesh_client.cloud.default import Default

def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result

class Test_default():
    """

    """


    def setup(self):
        pass




    def test_001(self):
        """
        delete defaults
        :return:
        """
        HEADING()

        Default.clear()
        print(Default.list())
        assert True

    def _check(self, content):
        result = Default.list()
        print(result)
        assert content in str(result)


    def test_002(self):
        """
        set default cloud
        :return:
        """
        HEADING()

        name = "mycloud"
        Default.set_cloud(name)
        assert Default.get_cloud() == name

        self._check(name)

    def test_003(self):
        """
        set default image
        :return:
        """
        HEADING()

        name = "myimage"
        Default.set_image(name,"mycloud")
        assert Default.get_image("mycloud") == name

        self._check(name)

    def test_004(self):
        """
        set default flavor
        :return:
        """
        HEADING()

        name = "myflavor"
        Default.set_flavor(name,"mycloud")
        assert Default.get_flavor("mycloud") == name

        self._check(name)

    def test_005(self):
        """
        set default key
        :return:
        """
        HEADING()

        name = "mykey"
        Default.set_key(name)
        assert Default.get_key() == name

        self._check(name)

    def test_006(self):
        """
        set default key
        :return:
        """
        HEADING()

        name = "mygroup"
        Default.set_group(name)
        assert Default.get_group() == name

        self._check(name)

    def test_007(self):
        """
        set default variable
        :return:
        """
        HEADING()

        name = "myvar"
        value = "myvalue"
        cloud = "mycloud"
        Default.set(name, value, cloud)
        assert Default.get(name, cloud) == value

        self._check(value)


    def test_999(self):
        """
        clear the defaults
        :return:
        """
        HEADING()

        Default.clear()
        assert True

    '''
    def test_002(self):
        """
        tries to start a vm with an invalid image
        :return:
        """
        HEADING()
        result = run ("cm vm start --cloud=india --flavor=m1.medium --image=futuresystems/linux>windows")

        assert "not found" in result
    '''
