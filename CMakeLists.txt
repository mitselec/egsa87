cmake_minimum_required(VERSION 3.15)

project(egsa87 VERSION 1.2.0 LANGUAGES C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_library(egsa87 C/egsa87.c)
target_include_directories(egsa87 PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/C)

if(NOT WIN32)
    target_link_libraries(egsa87 PUBLIC m)
endif()

add_executable(egsa87_test C/egsa87_test.c)
target_link_libraries(egsa87_test PRIVATE egsa87)

if(MSVC)
    target_compile_options(egsa87 PRIVATE /W4)
    target_compile_options(egsa87_test PRIVATE /W4)
else()
    target_compile_options(egsa87 PRIVATE -Wall -Wextra)
    target_compile_options(egsa87_test PRIVATE -Wall -Wextra)
endif()
