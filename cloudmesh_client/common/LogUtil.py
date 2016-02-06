import inspect
import logging
from cloudmesh_base.util import path_expand
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.common.ConfigDict import ConfigDict

# define global format for logs
FORMAT = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(funcName)s() %(message)s"

# set global key for log
LOG_LEVEL_KEY = "log_level"

# default log level is ERROR
DEFAULT_LOG_LEVEL = "ERROR"

# define the logger
LOGGER = logging.getLogger('LogUtil')


class LogUtil(object):


    @staticmethod
    def save(cloudname):
        """
        save the loglevel for a cloud to the cloudmesh.yaml file
        :param cloudname: the name of the cloud
        """
        # TODO: BUG: this seems inconsistant as loglevels via default
        # can now be defined for clouds, but the yaml file only
        # specifies one value for all clouds.
        config = ConfigDict("cloudmesh.yaml")

        # get the log level from database
        log_level = Default.get(key=LOG_LEVEL_KEY,
                                cloud=cloudname) or \
                    DEFAULT_LOG_LEVEL

        # Update the cloudmesh config
        config["cloudmesh"]["logging"]["level"] = log_level

        # Save this into cloudmesh yaml
        config.save()


    @staticmethod
    def set_level(log_level, cloudname):
        """
        sets th eloglevel in teh database and the loglevel file from
        cloudmesh.yaml
        :param log_level: the loglevel
        :param cloudname: the cloudname
        :return:
        """
        # TODO: BUG: This seems inconsistent with our use as it mixes db and
        # cloudmesh.yaml.
        Default.set(key=LOG_LEVEL_KEY,
                    value=log_level,
                    cloud=cloudname)

        # get log level obj
        log_level_obj = LogUtil.get_level_obj(log_level)

        # Read the ConfigDict
        config = ConfigDict("cloudmesh.yaml")
        log_file = config["cloudmesh"]["logging"]["file"]

        # Set the logger config
        logging.basicConfig(format=FORMAT,
                            level=log_level_obj,
                            filename=path_expand(log_file))

        LOGGER.info("Set log level to: " + log_level)
        return "Ok."

    @staticmethod
    def get_level(cloudname):
        """
        get the log level from database
        :param cloudname: The name of the cloud
        :return: the log level
        """
        log_level = Default.get(key=LOG_LEVEL_KEY,
                                cloud=cloudname)

        LOGGER.info("Returning Log Level: " + log_level)

        # return the level
        return log_level

    @staticmethod
    def initialize_logging():
        """
        reads the log level from the cloudmesh.yaml file from
        cloudmesh.logging.level. If the value is not set the logging will be
        set to the default which is "ERROR"
        :return: the loglevel
        """
        config = ConfigDict("cloudmesh.yaml")
        log_level = config["cloudmesh"]["logging"]["level"] or \
                    DEFAULT_LOG_LEVEL

        # Get default cloud
        cloudname = Default.get_cloud()

        # Set the log level
        LogUtil.set_level(log_level, cloudname)

        return


    @staticmethod
    def get_logger():
        """
        get caller file name
        :return: file name based on the context where the logger is caller
        """

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        the_class = module.__name__

        # return logger object
        return logging.getLogger(the_class)


    @staticmethod
    def get_level_obj(log_level):
        """
        gets the log level when passing a string
        :param log_level: case insensitive string. Valid values are debug,
                          info, warning, critical, error
        :return: a logging level
        """
        # Return log level obj
        level = log_level.lower()
        if level == "debug":
            log_level = logging.DEBUG
        elif level == "info":
            level = logging.INFO
        elif log_level == "warning":
            level = logging.WARNING
        elif log_level == "critical":
            level = logging.CRITICAL
        elif level == "error":
            level = logging.ERROR
        else:
            level = logging.DEBUG

        return level