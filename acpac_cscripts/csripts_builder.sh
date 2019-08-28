rm -rf build
mkdir build
pushd build
cmake -G Ninja -D CMAKE_C_COMPILER=gcc-7 -D CMAKE_CXX_COMPILER=g++-7 ..
ninja && cp main ..
popd
