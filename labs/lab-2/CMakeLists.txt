cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

project(main)

find_library(GMP gmp)
find_library(PTHREAD_LIBRARY pthread)

add_executable(main main.cpp)

target_link_libraries(main ${GMP} ${PTHREAD_LIBRARY})
