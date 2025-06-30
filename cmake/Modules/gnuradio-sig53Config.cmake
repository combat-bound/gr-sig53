find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_SIG53 gnuradio-sig53)

FIND_PATH(
    GR_SIG53_INCLUDE_DIRS
    NAMES gnuradio/sig53/api.h
    HINTS $ENV{SIG53_DIR}/include
        ${PC_SIG53_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_SIG53_LIBRARIES
    NAMES gnuradio-sig53
    HINTS $ENV{SIG53_DIR}/lib
        ${PC_SIG53_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-sig53Target.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_SIG53 DEFAULT_MSG GR_SIG53_LIBRARIES GR_SIG53_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_SIG53_LIBRARIES GR_SIG53_INCLUDE_DIRS)
