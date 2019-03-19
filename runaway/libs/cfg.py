# coding=utf-8
'''
加载配置文件
'''

import sys
import os

Module = type(sys)
modules = {}


def cfgLoad(fullpath, env={}, module=Module):
    try:
        code = open(fullpath).read()
    except IOError:
        raise ImportError('No module named  %s') % fullpath
    filename = os.path.basename(fullpath)

    try:
        return modules[filename]
    except KeyError:
        pass

    m = module(filename)
    m.__module_class__ = module
    m.__file__ = fullpath

    m.__dict__.update(env)

    exec compile(code, filename, 'exec') in m.__dict__
    modules[filename] = m
    return m


def cfgReload(m):

    fullpath = m.__file__

    try:
        code = open(fullpath).read()
    except IOError:
        raise ImportError('No module named  %s') % fullpath

    env = m.__dict__
    module_class = m.__module_class__

    filename = os.path.basename(fullpath)
    m = module_class(filename)

    m.__file__ = fullpath
    m.__dict__.update(env)
    m.__module_class__ = module_class

    exec compile(code, filename, 'exec') in m.__dict__
    modules[filename] = m

    return m


AppDIR = os.path.dirname(os.path.realpath(__file__))
AppRoot = os.path.dirname(os.path.dirname(AppDIR))
RUNAWAY_CONF_DIR = os.environ['RUNAWAY_CONF_DIR']
# 配置文件读取
if not RUNAWAY_CONF_DIR.endswith(os.sep):
    RUNAWAY_CONF_DIR = RUNAWAY_CONF_DIR + os.sep

CONF_NAME = 'settings.cfg'

CONF_FILE = os.path.join(RUNAWAY_CONF_DIR, CONF_NAME)
if not os.path.exists(CONF_FILE):
    print '......config file not found! %s' % CONF_FILE
    sys.exit(1)

try:
    conf = cfgLoad(CONF_FILE)
except SyntaxError as e:
    print '......config file SyntaxError! %s' % str(e)
    sys.exit(1)
except IOError as e:
    print '......config file IOError! %s' % str(e)
    sys.exit(1)
except NameError as e:
    print '......config file NameError! %s' % str(e)
    sys.exit(1)
except Exception as e:
    print '......config file OtherError! %s' % str(e)
    sys.exit(1)

if __name__ == "__main__":
    print conf.__dict__
