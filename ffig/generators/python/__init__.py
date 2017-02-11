from python2 import py2_generator
from python3 import py3_generator

def setup_plugin(context):
    context.register(py2_generator, ['py.tmpl'])
    context.register(py3_generator, ['py3.tmpl'])
