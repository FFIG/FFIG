#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include <catch.hpp>
#include <string>
#include "Tree_cpp.h"

using CPP_API::Tree;

TEST_CASE("Test subtree access", "[cpp_api::tree]")
{
  auto root = Tree(3);
  auto left = root.left_subtree();
  
  REQUIRE(left.data());
}
