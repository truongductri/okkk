import sys
import os
sys.path.append(os.getcwd()+os.sep+"packages")
import config_reader
# config_reader.load("local")
config_reader.load("server172_16_7_67")
from quicky import tenancy
tenancy.set_schema("hrm")
from qexcel import writers
import qmongo
qmongo.set_db_context("mongodb://sys:123456@172.16.7.67:27017/lms:lv")

