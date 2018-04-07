# Customization points for type handling

* Proposal: FFIG-0001
* Author: Jonathan B Coe
* Reviewer: Unassigned
* Status: Draft

# Introduction

We want to be able to specify custom binding generation for user-defined types
so that they can be handled in unusual or target-language-specific ways.

# Motivation

FFIG does not (yet) support generating bindings for C++ library types, nor does
FFIG allow a user to specify how a user-defined-type should be exposed: there
is only FFIG's way. Solving both of these problems in one go would be useful.

A mechanism for specifying customisation points would allow users to specify
how types should be handled and could be used to supply
target-langauge-specific bindings for standard library types like
`std::vector<double>`. Such a mechanism could be used to support the C++
Standard Library, Abseil and Boost [FIXME(jbcoe):References needed].

# Detailed Design

Piggyback the filters mechanism to specify how a type should be bound in
various different contexts.  If no custom binding is found for a type in a
given context then fall back to FFIG's standard way of handling user-defined
types - hoist them onto the heap and expose them through a wrapped pointer. 

The custom bindings could be expressed using clang's matcher syntax so that
types can be matched in a C++-aware way. There is discussion about adding AST
matcher support to libclang [FIXME(jbcoe):Reference needed].

TODO - add example

# Alternatives considered

* Use a regex to match types rather than a clang C++ AST matcher.

* Hard-code type handling into FFIG filters.

* Require users to modify and maintain custom filters.

# Open questions

* What are the different contexts for which bindings are generated?

* What would the syntax look like?

