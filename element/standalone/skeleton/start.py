# -*- coding: UTF-8 -*-
import sys, logging, os, argparse, ioc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--verbose', '-v', action='count', help="verbose level", default=False)
    parser.add_argument('--debug', '-d', help="debug mode", action='store_true')
    parser.add_argument('--env', '-e', help="Define the environement", default='dev')
    
    options, argv = parser.parse_known_args(sys.argv)

    parameters = {
        'ioc.debug': options.debug,
        'ioc.env':   options.env,
        'project.root_folder': os.path.dirname(os.path.realpath(__file__))
    }
    
    files = [
        '%s/config/config.yml' % (parameters['project.root_folder']),
        '%s/config/services.yml' % (parameters['project.root_folder']),
        '%s/config/parameters_%s.yml' % (parameters['project.root_folder'], parameters['ioc.env']),
    ]

    logger = logging.getLogger('app')

    if options.verbose:
        logger.level = logging.DEBUG
        logging.basicConfig(level=logging.DEBUG)


    container = ioc.build(files, logger=logger, parameters=parameters)

    if not container.has('ioc.extra.command.manager'):
        sys.stdout.write(
        """
Error: No command manager defined, please create your own 
custom bootstrap script or add the ``ioc.extra.command:`` 
key into your configuration script.

--
Python IoC - Thomas Rabaix <thomas.rabaix@gmail.com>

        """
        )

        sys.exit(1)

    command_manager = container.get('ioc.extra.command.manager')

    sys.exit(command_manager.execute(sys.argv, sys.stdout))
