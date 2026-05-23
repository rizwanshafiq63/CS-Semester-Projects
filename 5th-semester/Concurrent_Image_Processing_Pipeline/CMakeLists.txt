cmake_minimum_required(VERSION 3.10)
project(ConcurrentImagePipeline LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Only core image I/O modules (avoids optional viz/hdf dependencies)
find_package(OpenCV REQUIRED COMPONENTS core imgcodecs imgproc)

add_executable(image_pipeline main.cpp)

target_include_directories(image_pipeline PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(image_pipeline PRIVATE ${OpenCV_LIBS} pthread rt)
