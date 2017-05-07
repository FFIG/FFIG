#include <memory>
#include <random>

#ifdef __clang__
#define C_API __attribute__((annotate("GENERATE_C_API")))
#else
#define C_API
#endif

static std::mt19937 mt;
static std::uniform_int_distribution<int> d(1,10);
static auto gen = []{return d(mt);};

class C_API Tree
{
  int data_;
  std::unique_ptr<Tree> left_;
  std::unique_ptr<Tree> right_;

  public:

  Tree(int levels=0)
  {
    data_ = gen();
    if ( levels <= 0 ) return;
    left_ = std::make_unique<Tree>(levels-1);
    right_ = std::make_unique<Tree>(levels-1);
  }

  const Tree* left_subtree() const
  {
    return left_.get();
  }

  const Tree* right_subtree() const
  {
    return right_.get();
  }

  void erase_data() 
  {
    data_ = 0;
  }

  int data() const
  {
    return data_;
  }
  
  void set_data(int x)
  {
    data_ = x;
  }

};

