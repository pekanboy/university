cmake_minimum_required(VERSION 3.13)  # CMake version check
project(simple_example)               # Create project "simple_example"
set(CMAKE_C_STANDARD 11)            # Enable c++14 standard
set(SER 1)
# Add executable target with source files listed in SOURCE_FILES variable
add_executable(lab2 lab2/main.c)
add_executable(lab1 lab1/main.c)
add_executable(lab3 lab3/main.c)