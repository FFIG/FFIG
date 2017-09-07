import os
import sys
from ffig.clang.cindex import AccessSpecifier, CursorKind, TypeKind, Diagnostic


def _get_annotations(node):
    return [c.displayname for c in node.get_children()
            if c.kind == CursorKind.ANNOTATE_ATTR]


class Type:

    def __init__(self, cindex_type):
        self.kind = cindex_type.kind
        self.name = cindex_type.spelling
        self.is_pointer = self.kind == TypeKind.POINTER
        self.is_reference = self.kind == TypeKind.LVALUEREFERENCE
        self.is_const = cindex_type.is_const_qualified()
        if self.is_pointer or self.is_reference:
            self.pointee = Type(cindex_type.get_pointee())
        else:
            self.pointee = None

    def __repr__(self):
        return "<cppmodel.Type {}>".format(self.name)

    def __str__(self):
        return self.name


class Member:

    def __init__(self, cursor):
        self.type = Type(cursor.type)
        self.name = cursor.spelling


class FunctionArgument:

    def __str__(self):
        if self.name is None:
            return "<cppmodel.FunctionArgument self.type.name>"
        return "<cppmodel.FunctionArgument {} {}>".format(self.type, self.name)

    def __init__(self, type, name=None):
        self.type = type
        self.name = name or None


class _Function(object):

    def __init__(self, cursor, force_noexcept):
        self.name = cursor.spelling
        arguments = [x.spelling or None for x in cursor.get_arguments()]
        argument_types = [Type(x) for x in cursor.type.argument_types()]

        # FIXME: Get noexcept info from the clang.cindex cursor
        self.is_noexcept = force_noexcept
        self.return_type = Type(cursor.type.get_result())
        self.arguments = []
        self.annotations = _get_annotations(cursor)

        for t, n in zip(argument_types, arguments):
            self.arguments.append(FunctionArgument(t, n))

    def __repr__(self):
        r = '{} {}({})'.format(self.return_type.name, str(self.name),
                               ', '.join([a.type.name for a in self.arguments]))
        if self.is_noexcept:
            r = r + " noexcept"
        return r


class Function(_Function):

    def __init__(self, cursor, namespaces=[], force_noexcept=False):
        _Function.__init__(self, cursor, force_noexcept)
        self.namespace = '::'.join(namespaces)
        if self.namespace:
            self.qualified_name = '::'.join([self.namespace, self.name])
        else:
            self.qualified_name = self.name

    def __repr__(self):
        s = _Function.__repr__(self)
        return "<cppmodel.Function {}>".format(s)

    def __eq__(self, f):
        if self.name != f.name:
            return False
        if self.namespace != f.namespace:
            return False
        if len(self.arguments) != len(f.arguments):
            return False
        for x, fx in zip([arg.type for arg in self.arguments],
                         [arg.type for arg in f.arguments]):
            if x.name != fx.name:
                return False
        return True


class Method(_Function):

    def __init__(self, cursor, force_noexcept=False):
        _Function.__init__(self, cursor, force_noexcept)
        self.is_const = cursor.is_const_method()
        self.is_virtual = cursor.is_virtual_method()
        self.is_pure_virtual = cursor.is_pure_virtual_method()
        self.is_public = (cursor.access_specifier == AccessSpecifier.PUBLIC)

    def __repr__(self):
        s = _Function.__repr__(self)
        if self.is_const:
            s = '{} const'.format(s)
        if self.is_pure_virtual:
            s = 'virtual {} = 0'.format(s)
        elif self.is_virtual:
            s = 'virtual {}'.format(s)
        return "<cppmodel.Method {}>".format(s)


class Class(object):

    def __repr__(self):
        return "<cppmodel.Class {}>".format(self.name)

    def __init__(self, cursor, namespaces, force_noexcept=False):
        self.name = cursor.spelling
        self.namespace = '::'.join(namespaces)
        if self.namespace:
            self.qualified_name = '::'.join([self.namespace, self.name])
        else:
            self.qualified_name = self.name
        self.constructors = []
        self.methods = []
        self.members = []
        self.annotations = _get_annotations(cursor)
        self.base_classes = []
        # FIXME: populate these fields with AST info
        self.source_file = str(cursor.location.file)
        self.source_line = int(cursor.location.line)
        self.source_column = int(cursor.location.column)

        for c in cursor.get_children():
            if c.kind == CursorKind.CXX_METHOD and c.type.kind == TypeKind.FUNCTIONPROTO:
                f = Method(c, force_noexcept)
                self.methods.append(f)
            elif c.kind == CursorKind.CONSTRUCTOR and c.type.kind == TypeKind.FUNCTIONPROTO:
                f = Method(c, force_noexcept)
                self.constructors.append(f)
            elif c.kind == CursorKind.FIELD_DECL:
                f = Member(c)
                self.members.append(f)
            elif c.kind == CursorKind.CXX_BASE_SPECIFIER:
                self.base_classes.append(c.type.spelling)


class Model(object):

    def _check_translation_unit(self, translation_unit):
        if len([d for d in translation_unit.diagnostics if d.severity == Diagnostic.error]) != 0:
            e = "Compile errors in translation unit {}:".format(
                translation_unit.spelling)
            for d in translation_unit.diagnostics:
                e += "\n  {}".format(d)
            raise Exception(e)

    def __init__(self, translation_unit, force_noexcept=False):
        self._check_translation_unit(translation_unit)
        self.filename = translation_unit.spelling
        self.functions = []
        self.classes = []
        self.add_child_nodes(translation_unit.cursor, [], force_noexcept)

    def __repr__(self):
        return "<cppmodel.Model filename={}, classes={}, functions={}>".format(
            self.filename, [c.name for c in self.classes], [f.name for f in self.functions])

    def extend(self, translation_unit):
        m = Model(translation_unit)
        # Check for duplicates and inconsistencies.
        for new_class in m.classes:
            is_new = True
            for old_class in self.classes:
                if new_class.qualified_name == old_class.qualified_name:
                    if new_class.source_file != old_class.source_file:
                        raise Exception("Class {} is defined in multiple locations: {} {}".format(
                            old_class.qualified_name, old_class.source_file, new_class.source_file))
                    # Move on as there can only be one match
                    is_new = False
                    break

            if is_new:
                self.classes.append(new_class)

        # We only look at declarations for functions so won't raise exceptions
        for new_function in m.functions:
            is_new = True
            for old_function in self.functions:
                if new_function == old_function:
                    is_new = False
                    break
            if is_new:
                self.functions.append(new_function)

    def add_child_nodes(self, cursor, namespaces=[], force_noexcept=False):
        for c in cursor.get_children():
            if c.kind == CursorKind.CLASS_DECL or c.kind == CursorKind.STRUCT_DECL:
                self.classes.append(Class(c, namespaces, force_noexcept))
            if c.kind == CursorKind.FUNCTION_DECL and c.type.kind == TypeKind.FUNCTIONPROTO:
                self.functions.append(Function(c, namespaces, force_noexcept))
            elif c.kind == CursorKind.NAMESPACE:
                child_namespaces = list(namespaces)
                child_namespaces.append(c.spelling)
                self.add_child_nodes(c, child_namespaces)

        # Drop functions and classes with "__" prefixes as they are standard
        # library implementation details.
        self.functions = [
            f for f in self.functions if not f.name.startswith('__')]
        self.classes = [c for c in self.classes if not len(
            c.name) == 0 and not c.name.startswith('__')]
