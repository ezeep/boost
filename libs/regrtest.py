#!/usr/bin/python

# boost compilation regression test

# Usage: regrtest [*|compiler] [*|library/program]
#
# Default: regrtest * *
#
# Compilers:  bcc   = Borland 5.5.1
#             cw    = Metrowerks CodeWarrior
#             gcc   = GNU GCC
#             gcc-stlport  = GNU GCC with STLport library
#             como  = Comeau C++
#             vc    = Microsoft Visual C++
#             vcstlport  = Microsoft Visual C++ with STLport library
#             suncc = Sun's C++ compiler
#             kcc = KAI C++ 3.4g
#             cxx   = Compaq C++
#             irixcc = SGI IRIX CC
#
# Examples: regrtest
#           regrtest
#           regrtest gcc
#           regrtest * smart_ptr/smart_ptr_test.cpp
#           regrtest gcc smart_ptr/smart_ptr_test.cpp
#
# Note: use the following command line syntax if output is to be redirected:
#           python regrtest.py [*|compiler] [*|library/program]  >log 2>&1

# Revision history:
#  21 Jun 00 Redesign to allow specifying compiler and program (Beman Dawes)
#  18 Jun 00 Initial Version (Beman Dawes)

# The Metrowerks and Microsoft compilers require various environment variables be set.
#   See mwcc -help
#   See http://msdn.microsoft.com/library/devprods/vs6/visualc/vccore/_core_building_on_the_command_line.3a_.overview.htm
# Others:
#   See bcb4.hlp.  Don't bother with bcb4tools.hlp; it has a bad link to the command line options

import sys
import os
import time

#------------------------------------------------------------------------------#

def invoke( desc, command ):

  print " ", desc
  f.write( "<td>" )
  print "  ", command     #script debugging aid
  sys.stdout.flush()
  rs=os.system( command )
  print " return status: ", rs
  if rs==0:
    f.write( "yes" )
  else:
    f.write( "no" )
  f.write( "</td>\n" )

#------------------------------------------------------------------------------#

def compile( program ):

  fullpath= path + "/libs/" + program

  print
  print "*****", program, "*****"

  f.write( "<tr>\n" )
  f.write( "<td><a href=\"" + program + "\">" + program + "</a></td>\n" )

# ----------  Linux2 ---------- #

  if sys.platform == "linux2": 
    if compiler_arg == "*" or compiler_arg == "gcc":
      invoke( "GCC 2.95.2", 'g++ -ftemplate-depth-30 -c -I' + path + ' ' + fullpath )
    if compiler_arg == "*" or compiler_arg == "gcc-stlport":
      invoke( "GCC 2.95.2 STLport 4.0", 'g++ -V 2.95.2-stlport -c -ftemplate-depth-30 -I' + path + ' ' + fullpath )
#    if compiler_arg == "*" or compiler_arg == "gcc-exp":
#      invoke( "GCC pre-2.97 experimental", '/opt/exp/gcc/bin/g++ -ftemplate-depth-30 -I' + path + ' ' + fullpath )
    if compiler_arg == "*" or compiler_arg == "como":
      invoke( "Comeau C++ 4.2.44 beta3", 'como -c -I' + path + ' ' + fullpath)
#    if compiler_arg == "*" or compiler_arg == "occ":
#      invoke( "OpenC++ 2.5.9", 'occ -c --regular-c++ -I' + path + ' ' + fullpath)

# ----------- Solaris (Sun OS 5)/Sparc ------ #

  elif sys.platform == "sunos5":
    if compiler_arg == "*" or compiler_arg =="suncc":
	invoke("Sun WorkShop 6 2000/04/07 C++ 5.1", 'CC -c -I' + path + ' ' + fullpath )
    if compiler_arg == "*" or compiler_arg == "gcc":
      invoke( "GCC 2.95.2", 'g++ -Wall -pedantic -ftemplate-depth-30 -Wno-long-long -c -I' + path + ' ' + fullpath )
    if compiler_arg == "*" or compiler_arg == "kcc":
      invoke( "KCC 3.4g", 'KCC --strict_warnings -I' + path + ' ' + fullpath )

# --------- DEC Alpha ---------- #

  elif sys.platform == "osf1V5":
    if compiler_arg=="*" or compiler_arg=="cxx":
      invoke( "Compaq C++", "cxx -std strict_ansi -D__USE_STD_IOSTREAM -I" + path + " -c " + fullpath ) 
    if compiler_arg=="*" or compiler_arg=="cxx-clib":
      invoke( "Compaq C++ with <cXXX> headers", "cxx -std strict_ansi -D__USE_STD_IOSTREAM -I$HOME/include -I" + path + " -c " + fullpath )

# ---------- IRIX ---------------#

  elif sys.platform == "irix6":
    if compiler_arg=="*" or compiler_arg=="irixcc":
      invoke( "IRIX CC", "CC -LANG:std -I" + path + " -c " + fullpath )
    if compiler_arg=="*" or compiler_arg=="irixcc-clib":
      invoke( "IRIX CC with <cXXX> headers", "CC -LANG:std -I$HOME/include -I" + path + " -c " + fullpath )


# ----------- BeOS5/Intel ------ #
#
# currently this compiler fails so many tests that it may not be worth while
# reporting the results: most of these are as a result of broken C++ standard
# libraries and a non-standard <climits>, problems that the forthcoming
# gcc3 should fix (STLPort does not build on this platform).
#
  elif sys.platform == "beos":
    if compiler_arg=="*" or compiler_arg=="gcc":
      invoke( "GNU GCC", "c++ -ftemplate-depth-30 -Wall -I" + path + "  " + fullpath )
    if compiler_arg=="*" or compiler_arg=="gcc-sgi":
      invoke( "GNU GCC", "c++ -ftemplate-depth-30 -Wall -I/boot/home/config/stlport/stl330 -I" + path + "  " + fullpath )

# ----------  Windows ---------- #

  else:
#    if compiler_arg=="*" or compiler_arg=="bcc54":
#      bcc54_path=os.environ["BOOST_BCC54_PATH"]
#      invoke( "Borland C++ 5.4 up2", "\"" + bcc54_path + "/bcc32\" -I" + path + " -j10 -q " + fullpath )
    if compiler_arg=="*" or compiler_arg=="bcc":
      bcc55_path=os.environ["BOOST_BCC55_PATH"]
      invoke( "Borland C++ 5.5.1", "\"" + bcc55_path + "/bcc32\" -I" + path + " -j10 -q " + fullpath )

    # GCC 2.95.2 is looping on some tests, so only invoke if asked for by name
    #if compiler_arg=="*" or compiler_arg=="gcc":
    if compiler_arg=="gcc":
      # TODO: fix the absolute STLport paths
      invoke( "GNU GCC", "c++ -ftemplate-depth-30 -I" + path + " -IC:/stl/STLport-4.0b8/stlport  " + fullpath + "  c:/stl/STLport-4.0b8/lib/libstlport_gcc.a" )

    if compiler_arg=="*" or compiler_arg=="cw":
      invoke( "Metrowerks CodeWarrior", "mwcc -maxerrors 10 -cwd source -I- -I" + path + " " + fullpath )

#John Maddock says use /Zm400 switch; it increases compiler memory
    if compiler_arg=="*" or compiler_arg=="vc":
      invoke( "VC++ with MS library", 'cl /c /nologo /Zm400 /MDd /W3 /GR /GX /Zi /Od /GZ /I "' + path + '" /D "WIN32" /D "_DEBUG" /D "_MBCS" /D "_CONSOLE" ' + fullpath )
    if compiler_arg=="*" or compiler_arg=="vcstlport":
      stl=os.environ["BOOST_STLPORT_PATH"]
      invoke( "VC++ with STLport library", 'cl /c /nologo /Zm400 /MDd /W3 /GR /GX /Zi /Od /GZ /I "' + stl + '" /I "' + path + '" /D "WIN32" /D "_DEBUG" /D "_MBCS" /D "_CONSOLE" ' + fullpath )


  f.write( "</tr>\n" )

#------------------------------------------------------------------------------#

def library():

  print
  print "***** Boost Library *****"

  f.write( "<tr>\n" )
  f.write( "<td>Boost library build</td>\n" )

  #if compiler_arg=="*" or compiler_arg=="bcc32":
  #if compiler_arg=="*" or compiler_arg=="gcc":
  #if compiler_arg=="*" or compiler_arg=="cw":

  #if compiler_arg=="*" or compiler_arg=="vc":
  #  command='cl /nologo /MDd /W3 /GR /GX /Zi /Od /GZ /I "' + path + '" /D "WIN32" /D "_DEBUG" /D "_MBCS" /D "_LIB /c"'
  #	command=command + " " + path + "/libs/" + ...
  #  invoke( "VC++ with MS library", command )
	      
#    invoke( "MS Lib with MS library", 'lib /nologo /out:"boost_vc.lib" boost_timer_vc.obj boost_prg_timer_vc.obj boost_prg_display_vc.obj' )

  #if compiler_arg=="*" or compiler_arg=="vcstlport":

  f.write( "</tr>\n" )

#----------------------------------  main  ------------------------------------#

# set up environment variables

path=os.environ["BOOST_PATH"]

compiler_arg="*"
if len(sys.argv)>1:
  compiler_arg=sys.argv[1]

program_arg="*"
if len(sys.argv)>2:
  program_arg=sys.argv[2]

if sys.platform == "linux2":
  platform = "Linux/x86"
elif sys.platform == "sunos5":
  platform = "SunOS5/sparc"
elif sys.platform == "osf1V5":
  platform = "Compaq Tru64 Unix"
elif sys.platform == "irix6":
  platform = "SGI IRIX 6"
elif sys.platform == "beos":
  platform = "BeOS5/x86"
elif sys.platform == "win32":
  platform = "Windows"
  if os.name == "nt":
    platform = platform + " NT / Windows 2000"
else:
  print "**** Error: unknown platform ****"
  sys.exit(1)

f=open( "cs-" + sys.platform + ".html", "w" )

f.write( "<html>\n<head>\n<title>\nCompiler Status: " + platform + "\n</title>\n</head>" )
f.write( "<body bgcolor=\"#FFFFFF\" text=\"#000000\">\n" )
f.write( "<h1><img border=\"0\" src=\"../c++boost.gif\" width=\"277\" height=\"86\"></h1>\n" )
f.write( "<h1>Compiler Status: " + platform + "</h1>\n" )
f.write( "<p><b>Run Date:</b> " + time.strftime("%d %b %Y %H:%M GMT", time.gmtime(time.time())) + "</p>\n" )
f.write( "<p>\n" )
f.write( "<table border=\"1\" cellspacing=\"0\" cellpadding=\"5\">\n"  )
f.write( "<tr>\n" )
f.write( "<td>Program</td>\n" )

if sys.platform == "linux2": 
  if compiler_arg == "*" or compiler_arg == "gcc":
    f.write( "<td>GNU<br>GCC<br>2.95.2</td>\n" )
  if compiler_arg == "*" or compiler_arg == "gcc-stlport":
    f.write( "<td>GNU<br>GCC<br>2.95.2<br>STLport<br>4.0</td>\n" )
#  if compiler_arg == "*" or compiler_arg == "gcc-exp":
#    f.write( "<td>GNU<br>GCC<br>pre-2.97 experimental</td>\n" )
  if compiler_arg == "*" or compiler_arg == "como":
    f.write( "<td>Comeau C++<br>4.2.44 beta3<br>STLport<br>4.0</td>\n" )
#  if compiler_arg == "*" or compiler_arg == "occ":
#    f.write( "<td>OpenC++<br>2.5.9</td>\n" )
elif sys.platform == "sunos5":
  if compiler_arg == "*" or compiler_arg == "suncc":
    f.write( "<td>Sun C++<br>Sun WorkShop 6, C++ 5.1</td>\n" )
  if compiler_arg == "*" or compiler_arg == "gcc":
    f.write( "<td>GNU<br>GCC<br>2.95.2</td>\n" )
  if compiler_arg == "*" or compiler_arg == "kcc":
    f.write( "<td>KAI<br>KCC<br>3.4g</td>\n" )
elif sys.platform == "osf1V5":
  if compiler_arg == "*" or compiler_arg == "cxx":
    f.write( "<td>Compaq C++<br>6.2-024</td>\n" )
  if compiler_arg == "*" or compiler_arg == "cxx-clib":
    f.write( "<td>Compaq C++<br>6.2-024<br>clib</td>\n" )
elif sys.platform == "irix6":
  if compiler_arg == "*" or compiler_arg == "irixcc":
    f.write( "<td>SGI IRIX CC<br>7.3.1.1m</td>\n" )
  if compiler_arg == "*" or compiler_arg == "irixcc-clib":
    f.write( "<td>SGI IRIX CC<br>7.3.1.1m<br>clib</td>\n" )
elif sys.platform == "beos":
  if compiler_arg == "*" or compiler_arg == "gcc":
    f.write( "<td>GNUPro<br>GCC&nbsp;2.9</td>\n" )
  if compiler_arg == "*" or compiler_arg == "gcc-sgi":
    f.write( "<td>GNUPro<br>GCC&nbsp;2.9<br>+<br>SGI&nbsp;STL&nbsp;3.3</td>\n" )
else:
#  if compiler_arg=="*" or compiler_arg=="bcc54":
#    f.write( "<td>Borland<br>BCC<br>5.4 up2</td>\n" )
  if compiler_arg=="*" or compiler_arg=="bcc":
    f.write( "<td>Borland<br>BCC<br>5.5.1</td>\n" )

  # GCC 2.95.2 is looping on some tests, so only invoke if asked for by name
  #if compiler_arg=="*" or compiler_arg=="gcc":
  if compiler_arg=="gcc":
   f.write( "<td>GNU<br>GCC<br>2.95.2<br>STLport<br>4.0 beta 8</td>\n" )
  if compiler_arg=="*" or compiler_arg=="cw":
    f.write( "<td>Metrowerks<br>CodeWarrior<br>6.0</td>\n" )
  if compiler_arg=="*" or compiler_arg=="vc":
    f.write( "<td>Microsoft<br>VC++<br>6.0 SP4</td>\n" )
  if compiler_arg=="*" or compiler_arg=="vcstlport":
    f.write( "<td>Microsoft<br>VC++<br>6.0 SP4<br>STLport<br>4.0</td>\n" )

f.write( "</tr>\n" )

if  program_arg=="*":
  compile( "config/config_test.cpp" )
  compile( "array/array1.cpp" )
#  compile( "compose/compose1.cpp" )
  compile( "concept_check/concept_check_test.cpp")
  compile( "concept_check/class_concept_check_test.cpp")
  compile( "concept_check/concept_check_fail_expected.cpp")
  compile( "concept_check/class_concept_fail_expected.cpp")
  compile( "functional/function_test.cpp" )
  compile( "graph/test/graph.cpp" )
  compile( "integer/cstdint_test.cpp" )
  compile( "integer/integer_test.cpp" )
  compile( "integer/integer_traits_test.cpp" )
  compile( "rational/rational_example.cpp" )
  compile( "random/random_test.cpp" )
  compile( "random/random_demo.cpp" )
  compile( "regex/demo/regress/regex_test.cpp" )
  compile( "regex/demo/regress/wregex_test.cpp" )
  compile( "smart_ptr/smart_ptr_test.cpp" )
  compile( "static_assert/static_assert_test.cpp" )
#  compile( "utility/algo_opt_examples.cpp" )
  compile( "utility/call_traits_test.cpp" )
  compile( "utility/cast_test.cpp" )
  compile( "utility/compressed_pair_test.cpp" )
  compile( "utility/iterator_adaptor_test.cpp" )
  compile( "utility/iterators_test.cpp" )
  compile( "utility/operators_test.cpp" )
  compile( "utility/tie_example.cpp" )
  compile( "utility/type_traits_test.cpp" )
else:
  compile( program_arg )

f.write( "</table>\n" );

if sys.platform == "linux2":
  f.write( "<p>\nNotes: A hand-crafted &lt;limits&gt; Standard header has been applied to all configurations.\n" );
  f.write( "The tests were run on a GNU libc 2.2 system which has improved wide character support compared to previous versions.\n" )
elif sys.platform == "osf1V5" or sys.platform == "irix6":
  f.write( "<p>\nNote: For the 'clib' configuration, the missing new-style C library headers &lt;cXXX&gt; have been supplied.\n" )

f.write( "</body>\n</html>\n" )

# end

