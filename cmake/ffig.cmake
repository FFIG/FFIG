# ffig_add_library
# ----------------
#
# This module defines a function that allows the user to add a build target
# that constructs a shared library with a C-API and optional language bindings
# that make use of the C-API. 
#
# FIXME: Make output directory user-configurable.
# Currently the generated bindings and libraries go into ${CMAKE_CURRENT_BINARY_DIR}/generated.
#
# Usage:
#
# ffig_add_library(NAME myModuleName INPUTS myHeader.h RUBY PYTHON)
#
# This will create a build target called myModuleName_c which creates a shared library:
# * libmyModuleName.so on Linux
# * libmyModuleName.dylib on macOS
# * myModuleName.dll on Windows
#
# NAME is required, 
# FIXME: relax constraints on INPUTS
# INPUTS currently supports only a single header file (which must have only standard library includes).
#
# Optional bindings can be created by passing in any of the optional arguments:
# * RUBY - creates myModuleName.rb
# * PYTHON - creates myModuleName/{_py3.py,_py2.py,__init__.py}
# * LUA - creates myModuleName.lua (needs luajit)
# * CPP - creates myModuleName_cpp.h
# * CPP_MOCKS - creates myModuleName_mocks.h

function(ffig_add_library)
  set(options BOOST_PYTHON RUBY PYTHON CPP CPP_MOCKS GO LUA DOTNET D SWIFT JAVA)
  set(oneValueArgs NAME INPUTS)
  cmake_parse_arguments(ffig_add_library "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(module ${ffig_add_library_NAME})
  set(input ${ffig_add_library_INPUTS})

  # Always generate c-api bindings as all other bindings use them.
  set(ffig_invocation "-i;${input};-m;${module};-o;${CMAKE_CURRENT_BINARY_DIR}/generated;-b;_c.h.tmpl;_c.cpp.tmpl")
  set(ffig_outputs "${CMAKE_CURRENT_BINARY_DIR}/generated/${module}_c.h;${CMAKE_CURRENT_BINARY_DIR}/generated/${module}_c.cpp")  
  set(ffig_output_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")

  if(ffig_add_library_BOOST_PYTHON)
    set(ffig_invocation "${ffig_invocation};boost-python")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}_py.cpp")
  endif()
  if(ffig_add_library_RUBY)
    set(ffig_invocation "${ffig_invocation};ruby")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.rb")
  endif()
  if(ffig_add_library_LUA)
    set(ffig_invocation "${ffig_invocation};lua")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.lua")
  endif()
  if(ffig_add_library_DOTNET)
    set(ffig_invocation "${ffig_invocation};dotnet")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.cs")
  endif()
  if(ffig_add_library_PYTHON)
    set(ffig_invocation "${ffig_invocation};python")
    string(TOLOWER "${module}" module_lower)
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module_lower}/__init__.py")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module_lower}/_py2.py")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module_lower}/_py3.py")
  endif()
  if(ffig_add_library_CPP_MOCKS)
    set(ffig_invocation "${ffig_invocation};_mocks.h.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}_mocks.h")
  endif()
  if(ffig_add_library_CPP)
    set(ffig_invocation "${ffig_invocation};_cpp.h.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}_cpp.h")
  endif()
  if(ffig_add_library_GO)
    set(ffig_invocation "${ffig_invocation};go")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/src/${module}/${module}.go")
  endif()
  if(ffig_add_library_D)
    set(ffig_invocation "${ffig_invocation};d.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.d")
  endif()
  if(ffig_add_library_SWIFT)
    set(ffig_invocation "${ffig_invocation};swift")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.swift;${ffig_output_dir}/${module}-Bridging-Header.h")
  endif()
  if(ffig_add_library_JAVA)
    set(ffig_invocation "${ffig_invocation};java.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.java")
  endif()

  add_custom_command(OUTPUT ${ffig_outputs}
    COMMAND ${PYTHON_EXECUTABLE} -m ffig ${ffig_invocation}
    DEPENDS ${input} ${FFIG_SOURCE}
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    COMMENT "Generating FFIG bindings for ${input}: ${ffig_outputs}")

  # FIXME: This is a bit ugly. The header is copied next to the generated bindings.
  file(COPY ${input} DESTINATION ${ffig_output_dir}/)

  add_library(${module}_c SHARED ${input} ${ffig_output_dir}/${module}_c.h ${ffig_output_dir}/${module}_c.cpp)

  # FIXME: This is a bit ugly. The shared library is copied next to the generated bindings.
  add_custom_command(TARGET ${module}_c
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${module}_c> ${ffig_output_dir}/)

  if(ffig_add_library_PYTHON)
      # Run pycodestyle on generated Python. Ignore line-length errors,
      # as with generated code we have no control over the length of
      # type or function names supplied as input.
      add_custom_command(TARGET ${module}_c
          POST_BUILD
          COMMAND ${PYTHON_EXECUTABLE} -m pycodestyle --ignore=E501 ${ffig_output_dir}/${module_lower}
          DEPENDS ${ffig_outputs})
  endif()
endfunction()

