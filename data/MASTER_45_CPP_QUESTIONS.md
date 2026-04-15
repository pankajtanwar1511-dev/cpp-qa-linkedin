# 🎯 THE DEFINITIVE 45 C++ QUESTIONS
## Master Reference Document for LinkedIn Content Strategy

**Purpose:** Curated set of 45 unique, high-quality C++ questions covering fundamental to advanced concepts.
**Target Audience:** C++ developers from beginner to senior level
**Educational Value:** Each question teaches a real concept with practical relevance
**Interview Coverage:** Based on actual FAANG+ interview questions

---

## 📚 TABLE OF CONTENTS

1. [OOP & Polymorphism (8 Questions)](#category-1-oop--polymorphism)
2. [Memory Management & RAII (6 Questions)](#category-2-memory-management--raii)
3. [Smart Pointers (3 Questions)](#category-3-smart-pointers)
4. [Move Semantics & References (4 Questions)](#category-4-move-semantics--references)
5. [Templates & Metaprogramming (4 Questions)](#category-5-templates--metaprogramming)
6. [Type Deduction (3 Questions)](#category-6-type-deduction)
7. [Containers & STL (3 Questions)](#category-7-containers--stl)
8. [Multithreading (5 Questions)](#category-8-multithreading)
9. [Modern C++ Features (4 Questions)](#category-9-modern-c-features)
10. [Design Patterns (3 Questions)](#category-10-design-patterns)
11. [Low-Level Internals (2 Questions)](#category-11-low-level-internals)

---

# CATEGORY 1: OOP & Polymorphism

## Question 1: Private Virtual Functions Work!

**Source:** `chapter_1_oops/topic_1_practice.md` Q3
**Concept:** Virtual dispatch ignores access specifiers
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>
using namespace std;

class A {
private:
    virtual void func() { cout << "A::func" << endl; }
public:
    void call() { func(); }
};

class B : public A {
public:
    void func() { cout << "B::func" << endl; }
};

int main() {
    A* ptr = new B();
    ptr->call();
    delete ptr;
}
```

### Answer:
```
B::func
```

### Explanation:
- Virtual functions work even when declared private
- Access specifiers are checked at compile-time, but virtual dispatch happens at runtime
- `call()` is public, so it can be called from main. Inside call(), it invokes func()
- Even though func() is private in A, the virtual table resolves it to B::func at runtime
- Runtime polymorphism doesn't care about access levels

### Why This Matters:
- Many developers don't know private virtuals work
- Shows the clear separation between compile-time access control and runtime polymorphism
- This is the basis of Template Method design pattern
- Common interview question at top companies

---

## Question 2: Object Slicing Kills Polymorphism

**Source:** `chapter_1_oops/topic_2_practice.md` Q4
**Concept:** Pass by value slices derived objects
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class A {
public:
    virtual void show() { std::cout << "A\n"; }
};

class B : public A {
public:
    void show() { std::cout << "B\n"; }
};

void func(A a) {
    a.show();
}

int main() {
    B b;
    func(b);
}
```

### Answer:
```
A
```

### Explanation:
- func() takes parameter by value, not by reference or pointer
- When you pass B object to func(A a), object slicing happens
- Only the A part of B gets copied. B's data and virtual table pointer are lost
- Now it's just a plain A object, virtual function doesn't work
- To fix this: change func signature to func(A& a) or func(A* a)

### Why This Matters:
- Common polymorphism bug for beginners
- Causes subtle bugs in production - code compiles but doesn't behave as expected
- Classic interview question at Amazon, Microsoft, Bloomberg
- Teaches proper parameter passing for polymorphic objects

---

## Question 3: Virtual Functions in Constructors Don't Dispatch

**Source:** `chapter_1_oops/topic_2_practice.md` Q7
**Concept:** Constructor virtual calls don't use derived version
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class A {
public:
    A() { show(); }
    virtual void show() { std::cout << "A\n"; }
};

class B : public A {
public:
    void show() override { std::cout << "B\n"; }
};

int main() {
    B b;
}
```

### Answer:
```
A
```

### Explanation:
- When A's constructor runs, the B part hasn't been constructed yet
- At that point, the object is just type A
- So show() resolves to A::show(), not B::show()
- This is actually a safety feature - prevents calling functions on uninitialized derived parts
- Virtual dispatch only works after the object is fully constructed

### Why This Matters:
- C++ language design decision for safety
- Prevents accessing uninitialized memory
- Common confusion point
- Tests deep understanding of construction order

---

## Question 4: Default Arguments with Virtual Functions

**Source:** `chapter_1_oops/topic_2_practice.md` Q8
**Concept:** Default args resolved at compile-time, not runtime
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class Base {
public:
    virtual void display(int x = 10) {
        std::cout << "Base: " << x << "\n";
    }
};

class Derived : public Base {
public:
    void display(int x = 20) override {
        std::cout << "Derived: " << x << "\n";
    }
};

int main() {
    Base* ptr = new Derived();
    ptr->display();
    delete ptr;
}
```

### Answer:
```
Derived: 10
```

### Explanation:
- The function called is determined at runtime - Derived::display gets called
- But default arguments are determined at compile-time based on pointer type
- ptr is Base*, so compiler uses Base's default value (x=10)
- Result: Derived's function executes with Base's default argument
- Default arguments don't participate in virtual dispatch

### Why This Matters:
- Classic interview trap question
- Tests deep understanding of compile-time vs runtime resolution
- Can cause real-world bugs if you're not aware of this behavior
- Common at senior level interviews

---

## Question 5: Missing Virtual Destructor

**Source:** `chapter_1_oops/topic_2_practice.md` Q2
**Concept:** Non-virtual destructor skips derived cleanup
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class A {
public:
    A() { std::cout << "A\n"; }
    ~A() { std::cout << "~A\n"; }
};

class B : public A {
public:
    B() { std::cout << "B\n"; }
    ~B() { std::cout << "~B\n"; }
};

int main() {
    A* p = new B();
    delete p;
}
```

### Answer:
```
A
B
~A
```

### Explanation:
- Constructors run in order: A() first, then B()
- But destructors: Only ~A() is called, ~B() is completely skipped
- This is undefined behavior - if B had allocated resources, they would leak
- Fix: make ~A() virtual
- This is why you should always make destructors virtual in base classes used polymorphically

### Why This Matters:
- Common resource leak pattern in C++ code
- Undefined behavior that can crash in production
- Core C++ rule: always use virtual destructor for polymorphic base classes
- Asked in pretty much every systems programming interview

---

## Question 6: Non-Virtual Functions Use Static Binding

**Source:** `chapter_1_oops/topic_2_practice.md` Q20
**Concept:** Without virtual, pointer type determines function called
**Difficulty:** ⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class Base {
public:
    void func() { std::cout << "Base\n"; }
};

class Derived : public Base {
public:
    void func() { std::cout << "Derived\n"; }
};

int main() {
    Base* ptr = new Derived();
    ptr->func();
    delete ptr;
}
```

### Answer:
```
Base
```

### Explanation:
- func() is not virtual, so there's no runtime polymorphism
- ptr is Base*, so compiler resolves to Base::func() at compile-time (static binding)
- The actual object type doesn't matter without virtual keyword
- Derived::func() would only be called if you had Derived* ptr or Derived object
- To fix: add virtual keyword to Base::func()

### Why This Matters:
- Teaches difference between static and dynamic binding
- Common beginner mistake
- Performance consideration (virtual has overhead)
- Interview basic

---

## Question 7: Pure Virtual Can Have Implementation

**Source:** `chapter_1_oops/topic_2_practice.md` Q13
**Concept:** Pure virtual = 0 can still have body
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥

### Code:
```cpp
#include <iostream>

class A {
public:
    virtual void foo() = 0;
    ~A() { std::cout << "~A\n"; }
};

void A::foo() {
    std::cout << "A::foo implementation\n";
}

class B : public A {
public:
    void foo() override {
        A::foo();
        std::cout << "B::foo\n";
    }
};

int main() {
    A* ptr = new B();
    ptr->foo();
    delete ptr;
}
```

### Answer:
```
A::foo implementation
B::foo
~A
```

### Explanation:
- Pure virtual (= 0) can still have an implementation
- A::foo() is defined outside the class even though it's pure virtual
- B must override foo() (because it's pure virtual), but can call A::foo() explicitly
- This outputs both implementations
- Pure virtual forces derived classes to override, but base can still provide default behavior

### Why This Matters:
- Advanced pattern that most developers don't know about
- Useful when you want to force override but also provide optional default behavior
- Used in STL and framework code
- Shows deep C++ knowledge

---

## Question 8: Protected Copy Constructor Prevents Slicing

**Source:** `chapter_1_oops/topic_2_practice.md` Q18
**Concept:** Protected copy prevents pass-by-value
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class Base {
protected:
    Base(const Base&) = default;
public:
    Base() = default;
    virtual void show() const { std::cout << "Base\n"; }
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void show() const override { std::cout << "Derived\n"; }
};

void process(Base b) {
    b.show();
}

int main() {
    Derived d;
    process(d);
}
```

### Answer:
```
Compilation Error
```

### Explanation:
- Base copy constructor is protected, not public
- process(Base b) needs to copy Derived object to Base
- But copy constructor is not accessible from main()
- This is actually a design pattern to prevent accidental object slicing
- If you really need to pass Base, you must use reference or pointer

### Why This Matters:
- Intentional design pattern to prevent accidental slicing
- Shows you can use access control for API design
- Advanced C++ idiom used in production code
- Tests understanding of both access control and object-oriented design

---

# CATEGORY 2: Memory Management & RAII

## Question 9: Rule of Three Violation - Double Delete

**Source:** `chapter_2_memory_management/topic_1_practice.md` Q4
**Concept:** Default copy constructor = shallow copy = crash
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

struct Widget {
    int* data;
    Widget() : data(new int[10]) {}
    ~Widget() { delete[] data; }
};

int main() {
    Widget w1;
    Widget w2 = w1;  // Copy
}
```

### Answer:
```
Double delete / Crash at program exit
```

### Explanation:
- Default copy constructor does shallow copy
- After Widget w2 = w1, both w1.data and w2.data point to the same memory
- When scope ends, w2 is destroyed first and deletes the memory
- Then w1 is destroyed and tries to delete already-freed memory
- Double delete - undefined behavior, usually crashes
- Fix: implement proper copy constructor (deep copy) or delete it

### Why This Matters:
- Most C++ developers hit this bug at least once
- Teaches Rule of Three/Five
- Core memory management concept
- Common interview question at Amazon, Bloomberg

---

## Question 10: Exception in Constructor = No Destructor

**Source:** `chapter_10_raii_resource_management/topic_1_practice.md` Q3
**Concept:** Constructor throws → destructor never called
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class FileHandle {
    FILE* file;
public:
    FileHandle(const char* name) {
        file = fopen(name, "r");
        if (!file) throw std::runtime_error("Failed");
    }
    ~FileHandle() {
        if (file) {
            fclose(file);
            std::cout << "File closed\n";
        }
    }
};

void test() {
    try {
        FileHandle f("nonexistent.txt");
        std::cout << "File opened\n";
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << "\n";
    }
}

int main() {
    test();
}
```

### Answer:
```
Exception: Failed
```
(NO "File closed" message)

### Explanation:
- fopen fails because file doesn't exist, returns nullptr
- Constructor throws std::runtime_error
- Object construction never completes
- Destructor is NOT called (object was never fully constructed)
- No "File closed" message appears
- This is why RAII in constructors needs careful exception handling

### Why This Matters:
- Common interview question at top companies
- Critical RAII knowledge for C++ developers
- Shows why exception safety in constructors is important
- Resource leak pattern to avoid

---

## Question 11: new in Constructor + Exception = Leak

**Source:** `chapter_10_raii_resource_management/topic_1_practice.md` Q13
**Concept:** Resource acquired before throw = leaked
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class Resource {
    int* data;
public:
    Resource() : data(new int[100]) {
        std::cout << "Acquired\n";
        throw std::runtime_error("Error during init");
    }
    ~Resource() {
        delete[] data;
        std::cout << "Released\n";
    }
};

void test() {
    try {
        Resource r;
    } catch (...) {
        std::cout << "Caught\n";
    }
}

int main() {
    test();
}
```

### Answer:
```
Acquired
Caught
(Memory leak occurs)
```

### Explanation:
- new int[100] succeeds, memory is allocated
- Member initialization happens, data points to allocated memory
- "Acquired" prints
- Then exception is thrown in constructor body
- Constructor doesn't complete, so object doesn't fully exist
- Destructor is NOT called
- Memory is never freed - leak!
- Fix: use smart pointers or RAII members instead of raw new in constructors

### Why This Matters:
- Exception safety in constructors
- Solution: Use smart pointers or two-phase construction
- Real-world leak pattern
- Advanced C++ knowledge

---

## Question 12: Throwing from Destructor = std::terminate()

**Source:** `chapter_10_raii_resource_management/topic_1_practice.md` Q4
**Concept:** Never throw from destructors
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class Resource {
public:
    Resource() { std::cout << "Constructed\n"; }
    ~Resource() noexcept(false) {
        std::cout << "Destroying\n";
        throw std::runtime_error("Destructor throw");
    }
};

void test() {
    Resource r;
}

int main() {
    test();
}
```

### Answer:
```
Program calls std::terminate() and crashes
```

### Explanation:
- Resource is constructed, prints "Constructed"
- test() ends, Resource goes out of scope
- Destructor runs, prints "Destroying"
- Destructor throws exception
- C++ doesn't allow exceptions during stack unwinding
- Program calls std::terminate() and crashes immediately
- Rule: never throw exceptions from destructors

### Why This Matters:
- Core C++ rule
- Program termination behavior
- Exception safety fundamental
- Tests understanding of unwinding

---

## Question 13: RAII Exception Safety with Lock

**Source:** `chapter_10_raii_resource_management/topic_1_practice.md` Q7
**Concept:** RAII ensures cleanup even with exceptions
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>
#include <mutex>

class Lock {
    std::mutex& mtx;
public:
    Lock(std::mutex& m) : mtx(m) {
        mtx.lock();
        std::cout << "Locked\n";
    }
    ~Lock() {
        mtx.unlock();
        std::cout << "Unlocked\n";
    }
};

std::mutex globalMutex;

void function() {
    Lock lock(globalMutex);
    std::cout << "In critical section\n";
    throw std::runtime_error("Error");
}

int main() {
    try {
        function();
    } catch (...) {
        std::cout << "Caught\n";
    }
    return 0;
}
```

### Answer:
```
Locked
In critical section
Unlocked
Caught
```

### Explanation:
- Lock constructor acquires mutex, prints "Locked"
- "In critical section" prints
- Exception is thrown
- Stack unwinding begins
- Lock destructor is called automatically
- Mutex gets unlocked, prints "Unlocked"
- Then exception propagates to main
- This is the power of RAII - cleanup happens even with exceptions

### Why This Matters:
- Perfect example of RAII in action
- This is exactly why std::lock_guard exists
- Exception safety is critical in multithreaded code
- Prevents deadlocks in production systems

---

## Question 14: Partial Construction Cleanup

**Source:** `chapter_10_raii_resource_management/topic_1_practice.md` Q8
**Concept:** Members destroyed even if container constructor throws
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class Resource1 {
public:
    Resource1() { std::cout << "R1 acquired\n"; }
    ~Resource1() { std::cout << "R1 released\n"; }
};

class Resource2 {
public:
    Resource2() { std::cout << "R2 acquired\n"; }
    ~Resource2() { std::cout << "R2 released\n"; }
};

class Container {
    Resource1 r1;
    Resource2 r2;
public:
    Container() {
        std::cout << "Container constructed\n";
        throw std::runtime_error("Error");
    }
    ~Container() {
        std::cout << "Container destroyed\n";
    }
};

void test() {
    try {
        Container c;
    } catch (...) {
        std::cout << "Exception caught\n";
    }
}

int main() {
    test();
}
```

### Answer:
```
R1 acquired
R2 acquired
Container constructed
R2 released
R1 released
Exception caught
```

### Explanation:
- Members are constructed before constructor body runs
- r1 constructed: "R1 acquired"
- r2 constructed: "R2 acquired"
- Constructor body runs: "Container constructed"
- Constructor throws exception
- Container destructor is NOT called (construction didn't complete)
- But r1 and r2 are already constructed, so they ARE destroyed
- r2 destroyed first (reverse order): "R2 released"
- r1 destroyed: "R1 released"
- C++ ensures fully-constructed members get cleaned up even if container constructor fails

### Why This Matters:
- Advanced RAII behavior that prevents resource leaks
- C++ language guarantees that fully-constructed members get cleaned up
- Tests deep understanding of construction/destruction order
- Senior-level interview knowledge

---

# CATEGORY 3: Smart Pointers

## Question 15: Double shared_ptr from Raw Pointer

**Source:** `chapter_3_smart_pointers/topic_1_practice.md` Q6
**Concept:** Two shared_ptrs from same raw = two control blocks = double delete
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <memory>

int main() {
    int* raw = new int(100);
    std::shared_ptr<int> sp1(raw);
    std::shared_ptr<int> sp2(raw);  // Danger!
}
```

### Answer:
```
Double delete / Crash at program exit
```

### Explanation:
- sp1(raw) creates control block #1 for the raw pointer
- sp2(raw) creates control block #2 for the SAME raw pointer
- Two independent control blocks, both think they own the memory
- sp2 goes out of scope first, deletes the memory
- sp1 goes out of scope next, tries to delete already-freed memory
- Double delete, crash
- Fix: always use std::make_shared, or copy from existing shared_ptr

### Why This Matters:
- Common smart pointer bug that crashes at runtime
- Teaches how control blocks work internally
- Solution: always use std::make_shared or copy from existing shared_ptr
- Asked at trading firms and hedge funds

---

## Question 16: weak_ptr Breaks Circular References

**Source:** `chapter_3_smart_pointers/topic_1_practice.md` Q14
**Concept:** Circular shared_ptr = leak, weak_ptr fixes it
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <memory>
#include <iostream>

class B;

class A {
public:
    std::shared_ptr<B> ptrB;
    ~A() { std::cout << "~A\n"; }
};

class B {
public:
    std::shared_ptr<A> ptrA;  // Circular reference!
    ~B() { std::cout << "~B\n"; }
};

int main() {
    auto a = std::make_shared<A>();
    auto b = std::make_shared<B>();
    a->ptrB = b;
    b->ptrA = a;
}
```

### Answer:
```
(No output - memory leak!)
```

### Explanation:
- a and b both have reference count = 2 (one from local variable, one from the other object)
- Scope ends, local shared_ptrs are destroyed
- a's ref count: 2 → 1 (still held by b->ptrA)
- b's ref count: 2 → 1 (still held by a->ptrB)
- Neither reaches 0, so neither gets deleted
- Memory leak!
- Solution: use weak_ptr for one direction to break the cycle

### Why This Matters:
- Real-world smart pointer pattern
- Common in graph/tree structures
- Parent-child relationships
- Amazon/Microsoft favorite

---

## Question 17: unique_ptr Auto-Deletion

**Source:** `chapter_10_raii_resource_management/topic_1_practice.md` Q14
**Concept:** Automatic memory management with unique_ptr
**Difficulty:** ⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <memory>
#include <iostream>

std::unique_ptr<int> create() {
    return std::unique_ptr<int>(new int(42));
}

void test() {
    auto ptr = create();
    std::cout << *ptr << "\n";
}

int main() {
    test();
}
```

### Answer:
```
One allocation, one deallocation at end of test()
```

### Explanation:
- create() allocates int(42) with new
- Wraps it in unique_ptr for RAII
- Returns unique_ptr (uses move semantics)
- test() receives the unique_ptr
- Prints 42
- test() ends, ptr goes out of scope
- unique_ptr destructor automatically calls delete
- Memory is freed automatically, no manual delete needed
- This is the power of RAII with smart pointers

### Why This Matters:
- Modern C++ best practice
- Replaces raw new/delete
- Exception safe
- Teaches smart pointer basics

---

# CATEGORY 4: Move Semantics & References

## Question 18: Rvalue Reference is Lvalue

**Source:** `chapter_4_reference_copying_moving/topic_1_practice.md` Q3
**Concept:** Named rvalue ref has lvalue category
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

void process(int& lref) {
    std::cout << "Lvalue reference\n";
}

void process(int&& rref) {
    std::cout << "Rvalue reference\n";
}

int main() {
    int&& rref = 42;
    process(rref);
}
```

### Answer:
```
Lvalue reference
```

### Explanation:
- int&& rref = 42 creates an rvalue reference
- But rref itself is an lvalue (it has a name, you can take its address)
- process(rref) calls the lvalue overload
- This is mind-bending: named rvalue references are lvalues
- To pass it as rvalue: use process(std::move(rref))
- This is why std::move and std::forward exist

### Why This Matters:
- Surprises most developers when they first learn it
- Core concept for understanding move semantics correctly
- Explains why std::forward is necessary
- Advanced interview question that tests deep understanding

---

## Question 19: Perfect Forwarding

**Source:** `chapter_4_reference_copying_moving/topic_1_practice.md` Q10
**Concept:** std::forward preserves value category
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <utility>
#include <iostream>

void process(int& x) { std::cout << "Lvalue\n"; }
void process(int&& x) { std::cout << "Rvalue\n"; }

template<typename T>
void forward_wrapper(T&& arg) {
    process(std::forward<T>(arg));
}

int main() {
    int x = 10;
    forward_wrapper(x);       // Pass lvalue
    forward_wrapper(20);      // Pass rvalue
}
```

### Answer:
```
Lvalue
Rvalue
```

### Explanation:
- forward_wrapper(x): T is deduced as int&, std::forward<int&> returns lvalue reference
- forward_wrapper(20): T is deduced as int, std::forward<int> returns rvalue reference
- std::forward preserves the value category of the original argument
- Without forward, both would call lvalue overload (because arg is a named parameter)
- This is perfect forwarding - used extensively in template libraries

### Why This Matters:
- Used extensively in STL (emplace, make_shared, etc.)
- Essential pattern for writing generic template code
- Advanced move semantics topic
- Senior-level interview question

---

## Question 20: auto Strips References

**Source:** `chapter_6_type_system_casting/topic_1_practice.md` Q9
**Concept:** auto deduces value type, not reference
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

int main() {
    int x = 10;
    int& ref = x;

    auto a = ref;        // What type is a?
    auto& b = ref;       // What type is b?

    a = 20;
    b = 30;

    std::cout << x << "\n";
}
```

### Answer:
```
30
```

### Explanation:
- auto a = ref: auto deduces int (strips reference), so a is a copy
- auto& b = ref: auto& deduces int&, so b is a reference
- a = 20: modifies the copy, x remains unchanged
- b = 30: modifies x through the reference
- Final x value: 30
- Lesson: auto strips references by default, use auto& or auto&& to keep them

### Why This Matters:
- Common auto pitfall
- Real-world bug source
- Teaches auto deduction rules
- Modern C++ essential

---

## Question 21: Move from Moved-From Object

**Source:** `chapter_4_reference_copying_moving/topic_1_practice.md` Q13
**Concept:** Moved-from object in valid but unspecified state
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <string>
#include <iostream>

int main() {
    std::string s1 = "Hello";
    std::string s2 = std::move(s1);

    std::cout << "s1: " << s1 << "\n";      // What prints?
    std::cout << "s2: " << s2 << "\n";

    s1 = "World";                           // Safe?
    std::cout << "s1: " << s1 << "\n";
}
```

### Answer:
```
s1:
s2: Hello
s1: World
```

### Explanation:
- After std::move(s1), s1 is in valid but unspecified state
- Usually empty, but C++ doesn't guarantee what state it's in
- You can assign to it: s1 = "World" is perfectly safe
- You can destroy it safely
- But don't try to use its value (could be anything)
- Rule: moved-from objects are safe to assign or destroy, but don't access their values

### Why This Matters:
- Move semantics safety rules
- Common confusion point
- Proper resource management
- Standard library behavior

---

# CATEGORY 5: Templates & Metaprogramming

## Question 22: Template Metaprogramming - Compile-Time Fibonacci

**Source:** `chapter_7_templates_generics/topic_1_practice.md` Q7
**Concept:** Recursive template instantiation = compile-time computation
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

template<int N>
struct Power2 {
    static constexpr int value = 2 * Power2<N-1>::value;
};

template<>
struct Power2<0> {
    static constexpr int value = 1;
};

int main() {
    std::cout << Power2<10>::value << "\n";
}
```

### Answer:
```
1024
```

### Explanation:
- Template instantiation happens recursively at compile time
- Power2<10> = 2 * Power2<9> = 2 * 2 * Power2<8> = ... = 1024
- Base case: Power2<0> = 1 stops the recursion
- Entire computation happens at compile time
- At runtime, it's just a constant 1024 - zero cost
- This is template metaprogramming in action

### Why This Matters:
- Shows template power
- Compile-time optimization
- STL uses this heavily
- Advanced C++ technique

---

## Question 23: Template Partial Specialization

**Source:** `chapter_7_templates_generics/topic_1_practice.md` Q13
**Concept:** Specialization for pointer types
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

template<typename T>
struct TypeTraits {
    static constexpr bool isPointer = false;
};

template<typename T>
struct TypeTraits<T*> {
    static constexpr bool isPointer = true;
};

int main() {
    std::cout << TypeTraits<int>::isPointer << "\n";
    std::cout << TypeTraits<int*>::isPointer << "\n";
}
```

### Answer:
```
0
1
```

### Explanation:
- Primary template has isPointer = false
- Partial specialization TypeTraits<T*> has isPointer = true
- TypeTraits<int> matches primary template → false
- TypeTraits<int*> matches specialization → true
- This is exactly how std::is_pointer and other type traits work
- Partial specialization is key to implementing type traits in STL

### Why This Matters:
- Core STL technique
- Type traits implementation
- Template specialization mastery
- Advanced interview topic

---

## Question 24: CRTP Infinite Recursion

**Source:** `chapter_12_design_patterns/topic_3_crtp_pattern_practice.md` Q1
**Concept:** Same method name = infinite recursion via name hiding
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥

### Code:
```cpp
#include <iostream>

template <typename T>
class Base {
public:
    void process() {
        static_cast<T*>(this)->process();
    }
};

class Derived : public Base<Derived> {
public:
    void process() {
        std::cout << "Processing\n";
    }
};

int main() {
    Derived d;
    d.process();
}
```

### Answer:
```
Infinite recursion / Stack overflow
```

### Explanation:
- d.process() resolves to Base::process() (only one process() visible due to name hiding)
- Base::process() calls static_cast<Derived*>(this)->process()
- This again resolves to Base::process() due to name hiding
- Infinite recursion, stack overflow
- Fix: use different method names (processImpl in Derived, process in Base)
- CRTP pattern requires careful naming to avoid this trap

### Why This Matters:
- Common CRTP pitfall that causes stack overflow
- Advanced template technique used in performance-critical code
- Real production bug pattern
- Tests understanding of name hiding and CRTP

---

## Question 25: SFINAE - Substitution Failure is Not An Error

**Source:** `chapter_7_templates_generics/topic_1_practice.md` Q15
**Concept:** Failed template substitution removes overload, not error
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>
#include <type_traits>

template<typename T>
typename std::enable_if<std::is_integral<T>::value>::type
process(T value) {
    std::cout << "Integral: " << value << "\n";
}

template<typename T>
typename std::enable_if<std::is_floating_point<T>::value>::type
process(T value) {
    std::cout << "Float: " << value << "\n";
}

int main() {
    process(42);
    process(3.14);
}
```

### Answer:
```
Integral: 42
Float: 3.14
```

### Explanation:
- For process(42): int is integral
  - First overload: enable_if succeeds, function is available
  - Second overload: enable_if fails, silently removed from overload set (SFINAE)
- For process(3.14): double is floating point
  - First overload: enable_if fails, removed (SFINAE)
  - Second overload: enable_if succeeds, function is available
- No compilation error despite failed substitutions
- SFINAE = Substitution Failure Is Not An Error

### Why This Matters:
- Pre-C++20 constraint technique
- Foundational for concepts
- STL uses this everywhere
- Advanced template knowledge

---

# CATEGORY 6: Type Deduction

## Question 26: decltype(auto) with Parentheses

**Source:** `chapter_6_type_system_casting/topic_1_practice.md` Q5
**Concept:** Parentheses change return from int to int&
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

int global = 10;

decltype(auto) getVal() { return global; }     // What type?
decltype(auto) getRef() { return (global); }   // What type?

int main() {
    getVal() = 20;  // Compiles?
    getRef() = 20;  // Compiles?

    std::cout << global << "\n";
}
```

### Answer:
```
Compilation error at getVal() = 20
getRef() = 20 compiles, global becomes 20
```

### Explanation:
- getVal(): decltype(global) = int, returns value
- getRef(): decltype((global)) = int&, returns reference (parentheses change everything!)
- getVal() = 20: can't assign to temporary value, compilation error
- getRef() = 20: assigns through reference, global becomes 20
- One pair of parentheses completely changes the return type
- This is subtle and dangerous if you're not careful

### Why This Matters:
- Surprising behavior that catches many off guard
- C++14 feature that requires careful attention
- Subtle type deduction issue
- Senior-level interview question

---

## Question 27: decltype(x) vs decltype((x))

**Source:** `chapter_9_cpp11_features/topic_1_practice.md` Q5
**Concept:** Double parentheses make it a reference
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

int main() {
    int x = 10;

    decltype(x) a = 5;      // Type of a?
    decltype((x)) b = x;    // Type of b?

    a = 100;
    b = 200;

    std::cout << x << "\n";
}
```

### Answer:
```
200
```

### Explanation:
- decltype(x): x is a variable, type is int
- decltype((x)): (x) is an lvalue expression, type is int&
- a = 100: modifies copy, x unchanged
- b = 200: modifies x through reference
- Parentheses completely change the result
- decltype(x) gives declared type, decltype((x)) gives expression type

### Why This Matters:
- Subtle difference with huge impact
- C++11 type deduction
- Teaches expression categories
- Advanced knowledge

---

## Question 28: Lambda Capture by Value vs Reference

**Source:** `chapter_11_multithreading/topic_1_practice.md` Q8
**Concept:** [x] captures copy, [&x] captures reference
**Difficulty:** ⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

int main() {
    int x = 5;

    auto lambda = [x]() mutable {
        x = 10;
        std::cout << "Lambda: " << x << "\n";
    };

    lambda();
    std::cout << "Main: " << x << "\n";
}
```

### Answer:
```
Lambda: 10
Main: 5
```

### Explanation:
- [x] captures x by value (creates a copy)
- mutable keyword allows modifying the copy
- Lambda modifies its own copy: prints 10
- Original x is unchanged: prints 5
- To modify the original: use [&x] to capture by reference
- Common mistake when using lambdas with threads

### Why This Matters:
- Lambda capture mechanics
- Common bug with threads
- Modern C++ feature
- Practical everyday code

---

# CATEGORY 7: Containers & STL

## Question 29: Vector Braces vs Parentheses

**Source:** `chapter_8_stl_containers_algorithms/topic_1_practice.md` Q5
**Concept:** () = count constructor, {} = initializer list
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v1(5, 10);
    std::vector<int> v2{5, 10};

    std::cout << v1.size() << " " << v2.size() << "\n";

    for (int x : v1) std::cout << x << " ";
    std::cout << "\n";
    for (int x : v2) std::cout << x << " ";
}
```

### Answer:
```
5 2
10 10 10 10 10
5 10
```

### Explanation:
- v1(5, 10): Calls count constructor → 5 elements, each with value 10
- v2{5, 10}: Uses initializer list constructor → 2 elements: {5, 10}
- Braces vs parentheses give completely different results
- This is one of the most confusing aspects of modern C++
- Rule: () uses normal constructor, {} prefers initializer_list constructor

### Why This Matters:
- Very commonly misunderstood
- Causes bugs in production code
- Caveat of uniform initialization syntax
- Classic interview trap question

---

## Question 30: Iterator Invalidation

**Source:** `chapter_8_stl_containers_algorithms/topic_1_practice.md` Q8
**Concept:** push_back can invalidate iterators
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3};
    auto it = v.begin();

    v.push_back(4);

    std::cout << *it << "\n";  // Safe or UB?
}
```

### Answer:
```
Undefined behavior (likely crash or garbage)
```

### Explanation:
- it points to the first element
- push_back(4) may reallocate the vector if capacity is exceeded
- Reallocation invalidates all existing iterators
- Dereferencing it after reallocation is undefined behavior
- May crash, print garbage, or seem to work (depends on memory state)
- Fix: re-obtain iterator after push_back, or reserve capacity upfront

### Why This Matters:
- Common STL bug that causes crashes
- Real production issue
- Tests understanding of container internals
- Favorite at trading firms and banks

---

## Question 31: Erase-Remove Idiom

**Source:** `chapter_8_stl_containers_algorithms/topic_1_practice.md` Q13
**Concept:** erase needs remove first to actually delete elements
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <vector>
#include <algorithm>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3, 2, 4, 2, 5};

    // Wrong way:
    // v.erase(2);  // Won't work

    // Right way - erase-remove idiom:
    v.erase(std::remove(v.begin(), v.end(), 2), v.end());

    for (int x : v) std::cout << x << " ";
}
```

### Answer:
```
1 3 4 5
```

### Explanation:
- std::remove() moves non-matching elements to the front
- Returns iterator to new logical end
- But doesn't actually erase anything, just rearranges
- erase() then removes elements from that iterator to end
- This is the erase-remove idiom
- Common pattern for efficiently removing elements from vectors

### Why This Matters:
- Common STL pattern
- Algorithm composition
- Efficiency (single pass)
- Everyday usage

---

# CATEGORY 8: Multithreading

## Question 32: Thread Must Be Joined or Detached

**Source:** `chapter_11_multithreading/topic_1_practice.md` Q1
**Concept:** Joinable thread destructor = std::terminate()
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <thread>
#include <iostream>

void worker() {
    std::cout << "Working\n";
}

int main() {
    std::thread t(worker);
    // Missing join or detach
}
```

### Answer:
```
Program calls std::terminate() and aborts
```

### Explanation:
- Thread t is created and worker starts executing
- main() exits immediately without waiting
- Thread object t goes out of scope
- t is still joinable (neither joined nor detached)
- std::thread destructor checks if thread is joinable
- If joinable: calls std::terminate() and aborts the program
- Fix: either t.join() or t.detach() before scope ends

### Why This Matters:
- Most developers hit this at least once
- Thread lifecycle fundamental
- Common production crash
- Asked in pretty much every multithreading interview

---

## Question 33: Exception in Thread = Terminate

**Source:** `chapter_11_multithreading/topic_1_practice.md` Q10
**Concept:** Exceptions don't cross thread boundaries
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <thread>
#include <iostream>

int main() {
    std::thread t([]{ throw std::runtime_error("Error"); });
    t.join();
    std::cout << "Completed\n";
}
```

### Answer:
```
Program calls std::terminate()
```

### Explanation:
- Thread created with lambda that throws exception
- Lambda executes, throws std::runtime_error
- No try-catch inside the thread
- Uncaught exception in thread causes std::terminate()
- Program aborts immediately
- "Completed" never prints
- Exceptions don't cross thread boundaries
- Fix: wrap thread function body in try-catch

### Why This Matters:
- Common interview question at top companies
- Critical multithreading knowledge
- Exception safety is crucial in threaded code
- Can cause production crashes

---

## Question 34: Dangling Reference in Detached Thread

**Source:** `chapter_11_multithreading/topic_1_practice.md` Q13
**Concept:** Detached thread + local variable capture = UB
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <thread>
#include <chrono>
#include <iostream>

void dangerous() {
    int data = 100;
    std::thread t([&data]{
        std::this_thread::sleep_for(std::chrono::seconds(1));
        std::cout << data << "\n";
    });
    t.detach();
}

int main() {
    dangerous();
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
}
```

### Answer:
```
Undefined behavior (likely crash or garbage output)
```

### Explanation:
- dangerous() is called
- Local variable data = 100 created on stack
- Lambda captures data by reference: [&data]
- Thread created and starts
- t.detach() makes thread run independently
- dangerous() returns immediately
- data goes out of scope and is destroyed
- Thread is still running, sleeps for 1 second
- After sleep, thread tries to access data
- data is destroyed - dangling reference, undefined behavior
- Fix: capture by value [data] for detached threads

### Why This Matters:
- Production killer bug
- Teaches thread lifetime
- Real-world pattern
- System design interviews

---

## Question 35: Thread Arguments Passed by Value

**Source:** `chapter_11_multithreading/topic_1_practice.md` Q2
**Concept:** Default is copy, use std::ref for references
**Difficulty:** ⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <thread>
#include <iostream>

void increment(int x) {
    ++x;
}

int main() {
    int value = 10;
    std::thread t(increment, value);
    t.join();
    std::cout << value << "\n";
}
```

### Answer:
```
10
```

### Explanation:
- value is initialized to 10
- Thread created with std::thread t(increment, value)
- Arguments are passed by value by default
- value is copied to the thread
- increment() receives the copy, not a reference
- ++x modifies the copy, not original value
- Thread completes, t.join() waits for it
- Original value is still 10
- To modify original: use std::ref(value) when creating thread

### Why This Matters:
- Common thread bug
- Teaches thread argument semantics
- std::ref usage
- Practical multithreading

---

## Question 36: std::thread is Move-Only

**Source:** `chapter_11_multithreading/topic_1_practice.md` Q5
**Concept:** Cannot copy threads, only move
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥

### Code:
```cpp
#include <thread>

int main() {
    std::thread t1([]{ });
    std::thread t2 = t1;  // Compiles?
}
```

### Answer:
```
Compilation error
```

### Explanation:
- t1 is created with empty lambda
- Trying to copy-construct t2 from t1
- std::thread has deleted copy constructor
- Cannot copy threads - only one object can own a thread
- Thread ownership is exclusive
- Move-only type, similar to unique_ptr
- Fix: std::thread t2 = std::move(t1)

### Why This Matters:
- Move semantics application
- Resource ownership model
- Thread safety
- Modern C++ design

---

# CATEGORY 9: Modern C++ Features

## Question 37: C++20 Concepts - Clear Error Messages

**Source:** `chapter_19_cpp20_features/topic_1_concepts_constraints_practice.md` Q1
**Concept:** Concepts replace SFINAE with readable errors
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
#include <concepts>
#include <iostream>

template<std::integral T>
void process(T x) {
    std::cout << "Integral: " << x << "\n";
}

int main() {
    process(42);    // OK
    process(3.14);  // Error!
}
```

### Answer:
```
Compilation error: no matching function for process(double)
```

### Explanation:
- 42 is int, matches std::integral constraint, compiles fine
- 3.14 is double, does NOT match std::integral
- Compiler rejects process(3.14) with clear error: "constraints not satisfied"
- Before C++20 concepts, this would have been cryptic SFINAE error (hundreds of lines)
- Concepts give readable, human-friendly error messages
- This is one of C++20's best improvements

### Why This Matters:
- One of C++20's best features
- Future direction of C++
- Replaces complex SFINAE patterns
- Makes template errors actually readable

---

## Question 38: constexpr Requires Compile-Time Constant

**Source:** `chapter_13_compile_time_magic/topic_1_compile_time_programming_practice.md` Q1
**Concept:** constexpr variable needs constant initialization
**Difficulty:** ⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
constexpr int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    constexpr int y = add(5, x);  // Compiles?
}
```

### Answer:
```
Compilation Error
```

### Explanation:
- x is a runtime variable, value unknown at compile time
- constexpr int y requires compile-time constant initialization
- add(5, x) cannot be evaluated at compile time (x is runtime)
- Compiler error: "constexpr variable must be initialized by constant expression"
- Fix: make x constexpr, or remove constexpr from y

### Why This Matters:
- Common constexpr confusion
- Compile-time vs runtime
- Modern C++ feature
- Teaches constant evaluation

---

## Question 39: consteval Forces Compile-Time (C++20)

**Source:** `chapter_13_compile_time_magic/topic_1_compile_time_programming_practice.md` Q9
**Concept:** consteval = must evaluate at compile time, no exceptions
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
consteval int square(int x) {
    return x * x;
}

int main() {
    int runtime_val = 5;
    int result = square(runtime_val);  // Compiles?
}
```

### Answer:
```
Compilation Error
```

### Explanation:
- consteval (C++20) forces function to ALWAYS execute at compile time
- Stricter than constexpr (which can run at either compile-time or runtime)
- runtime_val is not a compile-time constant
- square(runtime_val) cannot be evaluated at compile time
- Compiler error: "consteval function requires constant expression"
- consteval guarantees zero runtime cost - computation must happen at compile time

### Why This Matters:
- C++20 cutting-edge feature
- Stricter than constexpr
- Guarantees zero runtime cost
- Future of C++

---

## Question 40: if constexpr Eliminates Dead Code

**Source:** `chapter_13_compile_time_magic/topic_1_compile_time_programming_practice.md` Q3
**Concept:** Compile-time branching removes unused code paths
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <type_traits>
#include <iostream>

template<typename T>
void process(T value) {
    if constexpr (std::is_integral_v<T>) {
        std::cout << value + 1 << "\n";
    } else {
        std::cout << value << "\n";
    }
}

int main() {
    process(42);
    process(std::string("hello"));
}
```

### Answer:
```
43
hello
```

### Explanation:
- if constexpr evaluates condition at compile time based on type T
- For process(42): T=int (integral), only value+1 branch is compiled
- For process("hello"): T=std::string (not integral), only value branch is compiled
- Discarded branch is not even instantiated - no errors even if it would be invalid
- Replaces SFINAE for many use cases
- Much cleaner and easier to understand than SFINAE

### Why This Matters:
- C++17 feature
- Modern template technique
- Cleaner than SFINAE
- Everyday template usage

---

# CATEGORY 10: Design Patterns

## Question 41: Singleton Race Condition

**Source:** `chapter_12_design_patterns/topic_1_singleton_pattern_practice.md` Q1
**Concept:** Non-atomic check-and-create = multiple instances + leak
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
class Manager {
    static Manager* instance;
    Manager() {}
public:
    static Manager* getInstance() {
        if (!instance) instance = new Manager();
        return instance;
    }
};
Manager* Manager::instance = nullptr;

// Multiple threads call getInstance() simultaneously
int main() {
    // Thread 1: Manager* m1 = Manager::getInstance();
    // Thread 2: Manager* m2 = Manager::getInstance();
    // What happens?
    return 0;
}
```

### Answer:
```
Race condition: multiple threads may create multiple instances
Memory leak: lost pointers to earlier allocations
```

### Explanation:
- Thread interleaving scenario:
  1. Thread A checks if (!instance) → true
  2. Thread B checks if (!instance) → true (before A assigns)
  3. Thread A executes instance = new Manager()
  4. Thread B also executes instance = new Manager()
  5. Result: Two Manager instances created, one pointer is lost
- Classic check-then-act race condition
- Singleton guarantee is broken - multiple instances exist
- Memory leak from lost pointer
- Fix: use mutex or C++11 magic statics (Meyers Singleton)

### Why This Matters:
- Classic multithreading bug
- Design pattern + concurrency
- Real-world production issue
- Asked at every company

---

## Question 42: Static Destruction Order Fiasco

**Source:** `chapter_12_design_patterns/topic_1_singleton_pattern_practice.md` Q2
**Concept:** Accessing destroyed static in destructor = UB
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

class Logger {
public:
    static Logger& getInstance() {
        static Logger instance;
        return instance;
    }
    void log(const char* msg) {
        std::cout << msg << "\n";
    }
    ~Logger() {
        std::cout << "~Logger\n";
    }
};

class Service {
public:
    static Service& getInstance() {
        static Service instance;
        return instance;
    }
    ~Service() {
        // Accessing Logger during Service destruction
        Logger::getInstance().log("Service destroyed");
    }
};

int main() {
    // Initialize both singletons
    Service::getInstance();
    Logger::getInstance();
    // What happens at program exit?
}
```

### Answer:
```
Undefined behavior: accessing destroyed Singleton
Possible crash or corruption during static destruction phase
```

### Explanation:
- Static locals are destroyed in reverse order of construction
- But order is NOT deterministic across different translation units
- Problem scenario:
  1. Logger is destroyed first (hypothetically)
  2. Service destructor runs
  3. Tries to call Logger::getInstance().log(...)
  4. Accessing destroyed Logger object - undefined behavior
- Possible outcomes: crash, corrupted memory, silent failure
- This is the static destruction order fiasco
- Fix: avoid accessing Singletons from destructors, or use never-destroyed pattern

### Why This Matters:
- Nightmare debugging scenario
- Only appears during shutdown
- Real-world gotcha
- Advanced C++ knowledge

---

## Question 43: Meyers Singleton Thread-Safety (C++11)

**Source:** `chapter_12_design_patterns/topic_1_singleton_pattern_practice.md` Q9
**Concept:** C++11 guarantees thread-safe static initialization
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥🔥

### Code:
```cpp
class Config {
public:
    static Config& getInstance() {
        static Config instance;
        return instance;
    }

private:
    Config() {}  // Constructor
};

int main() {
    // Multiple threads calling getInstance()
    Config& cfg1 = Config::getInstance();
    Config& cfg2 = Config::getInstance();
    // Is this thread-safe?
    return 0;
}
```

### Answer:
```
YES - Thread-safe in C++11 and later
```

### Explanation:
- C++11 introduced "magic statics" - thread-safe static local initialization
- Compiler automatically adds synchronization for static local initialization
- Only one thread will construct the instance
- Other threads wait until initialization completes
- After construction, zero overhead (no locking needed)
- This makes Meyers Singleton thread-safe by default in C++11+
- No manual mutex needed

### Why This Matters:
- Modern Singleton solution
- C++11 language guarantee
- No manual synchronization needed
- Interview favorite

---

# CATEGORY 11: Low-Level Internals

## Question 44: Struct Padding for Alignment

**Source:** `chapter_14_low_level_tricky/topic_1_low_level_internals_practice.md` Q2
**Concept:** Members padded for alignment requirements
**Difficulty:** ⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥🔥

### Code:
```cpp
#include <iostream>

struct S {
    char a;
    int b;
    char c;
};

int main() {
    std::cout << sizeof(S) << "\n";
}
```

### Answer:
```
12
```

### Explanation:
- Struct layout with padding for alignment:
  - char a (1 byte) + 3 padding bytes
  - int b (4 bytes, must be 4-byte aligned)
  - char c (1 byte) + 3 padding bytes
- Total: 1 + 3 + 4 + 1 + 3 = 12 bytes
- Reordering members can reduce size:
  - Put int b first, then both chars together → saves 4 bytes
- Padding ensures proper memory alignment for CPU access

### Why This Matters:
- Memory layout understanding
- Performance optimization
- Cache line efficiency
- Systems programming essential

---

## Question 45: Virtual Inheritance - Diamond Problem

**Source:** `chapter_14_low_level_tricky/topic_1_low_level_internals_practice.md` Q6
**Concept:** Virtual inheritance solves diamond with vbptr overhead
**Difficulty:** ⭐⭐⭐⭐⭐
**Interview Relevance:** 🔥🔥🔥

### Code:
```cpp
#include <iostream>

struct VBase { int v; };
struct A : virtual VBase { int a; };
struct B : virtual VBase { int b; };
struct C : A, B { int c; };

int main() {
    std::cout << sizeof(C) << "\n";
}
```

### Answer:
```
24-32 (platform dependent)
```

### Explanation:
- Virtual inheritance adds virtual base table pointers (vbptr) to A and B
- Typical 64-bit layout:
  - vbptr(8) + a(4) + padding(4) = 16
  - + vbptr(8) + b(4) + c(4) = 16
  - + v(4) + padding = variable
  - Total ≈ 24-32 bytes (platform dependent)
- VBase is shared - only one copy of v despite multiple inheritance paths
- Virtual inheritance solves diamond problem but adds overhead
- This is why virtual inheritance should be used carefully

### Why This Matters:
- Advanced inheritance pattern
- Diamond problem solution
- Memory layout complexity
- Deep C++ knowledge

---

## 🎯 USAGE GUIDELINES

### Photography Tips:
1. Use dark mode theme for code
2. Syntax highlighting essential
3. Keep code under 20 lines per image
4. Highlight critical lines with arrows
5. Add "?" emoji on confusing parts

### Posting Strategy:
1. **Post 3-4 questions per week**
2. **Rotate categories** to keep variety
3. **Start with fundamentals** (Q1-15) for first month
4. **Progress to advanced** (Q31-45) by month 3
5. **Reply within first hour** to all comments

### Engagement Tactics:
1. End with "Comment your answer 👇"
2. Reveal answer in comments after 30-60 min
3. Tag: 3-5 relevant hashtags max
4. Ask: "Have you been bitten by this bug?"
5. Frame: "$200k interview question" for advanced ones

---

## 📊 EXPECTED RESULTS

**Timeline:**
- **Weeks 1-2:** Build credibility (300-600 likes/post)
- **Weeks 3-4:** Gain momentum (600-1200 likes/post)
- **Weeks 5-6:** Viral potential (1000-3000 likes/post)
- **Weeks 7-9:** Thought leader (2000+ likes, 100+ comments)

**3-Month Goal:**
- 500+ new followers
- Established C++ expert status
- Consistent 1000+ engagement per post
- Speaking opportunities / consulting leads

---

**Document Version:** 1.0
**Last Updated:** 2026-04-15
**Total Questions:** 45
**Coverage:** C++98 to C++20
**Interview Relevance:** ⭐⭐⭐⭐⭐
