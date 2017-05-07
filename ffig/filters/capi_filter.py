import cppmodel
from cppmodel import TypeKind

# CPP filter to cast type if required


def restore_cpp_type(a):
    t = a.type
    n = a.name
    if t.kind == TypeKind.VOID:
        return n
    if t.kind == TypeKind.INT:
        return n
    if t.kind == TypeKind.DOUBLE:
        return n
    if t.kind == TypeKind.BOOL:
        return n
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return n
        if t.pointee.kind == TypeKind.RECORD:
            # This is a hack until we can get an unqualified type from libclang
            type_name = t.pointee.name.replace('const ', '')
            return '&(**static_cast<{}_ptr>({}))'.format(type_name, n)
    raise Exception(
        'Type {} has no defined C++ type restoration (adding one for primitives is trivial)'.format(t.name))


# C filter to convert C++ type to C equivalent
def to_c(t, m='Tree'):
    if t.kind == TypeKind.VOID:
        return 'void'
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'double'
    if t.kind == TypeKind.BOOL:
        return 'unsigned'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'const char*'
        if t.pointee.kind == TypeKind.RECORD:
            return '{}_{}'.format(m, t.pointee.name.replace('const ', ''))
    raise Exception('Type {} has no known c equivalent'.format(t.name))


def to_go(t):
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'float64'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'string'
        if t.pointee.kind == TypeKind.RECORD:
            return t.pointee.name.replace('const ', '')
    raise Exception('Type {} has no known Go equivalent'.format(t.name))


def to_go_convert(t):
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'float64'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'C.GoString'
        if t.pointee.kind == TypeKind.RECORD:
            return 'unsafe.Pointer'
    raise Exception('Type {} has no known Go equivalent'.format(t.name))


def to_go_method_name(m):
    '''
    Returns the method name with the first character uppercased.

    In Go, only entities with an uppercase first character are exposed in the
    module interface.
    '''
    return m.capitalize()


def go_object(a):
    '''
    In analogy to the `c_object` filter below, this returns `a.ptr` for objects
    of class type, and `a` for everything else.
    '''
    t = a.type
    n = a.name
    if t.kind == TypeKind.POINTER and t.pointee.kind == TypeKind.RECORD:
        return '{}.ptr'.format(n)
    else:
        return n

# C++ header filter to extract C type from C++ type


def c_object(a):
    t = a.type
    n = a.name
    if t.kind == TypeKind.VOID:
        return n
    if t.kind == TypeKind.INT:
        return n
    if t.kind == TypeKind.DOUBLE:
        return n
    if t.kind == TypeKind.BOOL:
        return n
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return n
        if t.pointee.kind == TypeKind.RECORD:
            return '{}->object_'.format(n)
    raise Exception(
        'No object extraction is defined for type {}'.format(
            t.name))


# Python filter to translate C-type to Python ctype type
def to_py3_ctype(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'c_int'
    if t.kind == TypeKind.DOUBLE:
        return 'c_double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'c_interop_string'
        if t.pointee.kind == TypeKind.RECORD:
            # This is a hack until we can get an unqualified type from libclang
            return t.pointee.name.replace('const ', '')
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_hint_type(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'float'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'str'
        if t.pointee.kind == TypeKind.RECORD:
            # This is encoding the assumption that the name of a binding class
            # is the same as the name of the underlying C++ class.
            return to_cpp_type(t)
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_output_py3_ctype(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'c_int'
    if t.kind == TypeKind.DOUBLE:
        return 'c_double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'c_interop_string'
        if t.pointee.kind == TypeKind.RECORD:
            return 'c_object_p'
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_py2_ctype(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'c_int'
    if t.kind == TypeKind.DOUBLE:
        return 'c_double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'c_char_p'
        if t.pointee.kind == TypeKind.RECORD:
            # This is a hack until we can get an unqualified type from libclang
            return t.pointee.name.replace('const ', '')
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_output_py2_ctype(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'c_int'
    if t.kind == TypeKind.DOUBLE:
        return 'c_double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'c_char_p'
        if t.pointee.kind == TypeKind.RECORD:
            return 'c_object_p'
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_cpp_type(t):
    if t.kind == TypeKind.VOID:
        return 'void'
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'const char *'
        if t.pointee.kind == TypeKind.RECORD:
            # This is a hack until we can get an unqualified type from libclang
            return t.pointee.name.replace('const ', '')
    raise Exception(
        'No c++ type equivalent is defined for type {} (adding one for primitives is trivial)'.format(t.name))


def to_ruby_type(t):
    if t.kind == TypeKind.VOID:
        return 'void'
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'string'
        if t.pointee.kind == TypeKind.RECORD:
            return 'pointer'
    raise Exception('No ruby equivalent is defined for type {}'.format(t.name))


def to_ruby_output_type(t):
    if t.kind == TypeKind.INT:
        return 'FFI::MemoryPointer.new :int'
    if t.kind == TypeKind.DOUBLE:
        return 'FFI::MemoryPointer.new :double'
    if t.kind == TypeKind.BOOL:
        return 'FFI::MemoryPointer.new :int'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'FFI::MemoryPointer.new(:pointer, 1)'
        if t.pointee.kind == TypeKind.RECORD:
            return 'FFI::MemoryPointer.new :pointer'
    raise Exception('No ruby equivalent is defined for type {}'.format(t.name))


def restore_ruby_type(t):
    if t.kind == TypeKind.INT:
        return 'get_int(0)'
    if t.kind == TypeKind.DOUBLE:
        return 'get_double(0)'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'read_pointer().read_string()'
        if t.pointee.kind == TypeKind.RECORD:
            return 'get_pointer(0)'
    raise Exception(
        'Type {} has no defined C++ type restoration (adding one for primitives is trivial)'.format(t.name))
