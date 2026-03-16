# Complexity Cheatsheet

Quick reference for time and space complexity of common Python operations.

## Python Built-in Data Structures

### List Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| `list[i]` | O(1) | O(1) | Index access |
| `list[i] = x` | O(1) | O(1) | Index assignment |
| `append(x)` | O(1)* | O(1) | Amortized |
| `pop()` | O(1) | O(1) | Remove last |
| `pop(i)` | O(n) | O(1) | Remove at index |
| `insert(i, x)` | O(n) | O(1) | Insert at index |
| `del list[i]` | O(n) | O(1) | Delete at index |
| `remove(x)` | O(n) | O(1) | Remove by value |
| `index(x)` | O(n) | O(1) | Find index |
| `in` (membership) | O(n) | O(1) | Linear search |
| `sort()` | O(n log n) | O(n) | Timsort |
| `reverse()` | O(n) | O(1) | In-place |
| `copy()` | O(n) | O(n) | Shallow copy |
| `len(list)` | O(1) | O(1) | Stored internally |

### Dictionary Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| `dict[key]` | O(1)* | O(1) | Hash table lookup |
| `dict[key] = val` | O(1)* | O(1) | Insert/update |
| `del dict[key]` | O(1)* | O(1) | Delete |
| `key in dict` | O(1)* | O(1) | Membership |
| `get(key)` | O(1)* | O(1) | Safe access |
| `pop(key)` | O(1)* | O(1) | Remove and return |
| `keys()` | O(1) | O(1) | View object |
| `values()` | O(1) | O(1) | View object |
| `items()` | O(1) | O(1) | View object |
| `copy()` | O(n) | O(n) | Shallow copy |
| `len(dict)` | O(1) | O(1) | Stored internally |

*Average case. Worst case O(n) with hash collisions.

### Set Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| `add(x)` | O(1)* | O(1) | Add element |
| `remove(x)` | O(1)* | O(1) | Remove (raises) |
| `discard(x)` | O(1)* | O(1) | Remove (silent) |
| `pop()` | O(1)* | O(1) | Remove arbitrary |
| `x in set` | O(1)* | O(1) | Membership |
| `union(s)` | O(len(s)+len(t)) | O(n) | `\|` operator |
| `intersection(s)` | O(min(len(s), len(t))) | O(n) | `&` operator |
| `difference(s)` | O(len(s)) | O(n) | `-` operator |
| `symmetric_difference(s)` | O(len(s)) | O(n) | `^` operator |
| `len(set)` | O(1) | O(1) | Stored internally |

### Tuple Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| `tuple[i]` | O(1) | O(1) | Index access |
| `in` (membership) | O(n) | O(1) | Linear search |
| `index(x)` | O(n) | O(1) | Find index |
| `count(x)` | O(n) | O(1) | Count occurrences |
| `len(tuple)` | O(1) | O(1) | Stored internally |

### String Operations

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| `s[i]` | O(1) | O(1) | Index access |
| `s[i:j]` | O(j-i) | O(j-i) | Slicing |
| `in` (substring) | O(n*m) | O(1) | Substring search |
| `find(x)` | O(n*m) | O(1) | Find substring |
| `split()` | O(n) | O(n) | Split string |
| `join(iter)` | O(n) | O(n) | Join strings |
| `replace()` | O(n) | O(n) | Replace substring |
| `strip()` | O(n) | O(n) | Remove whitespace |
| `len(s)` | O(1) | O(1) | Stored internally |

## Common Algorithm Patterns

### Searching

| Algorithm | Time (Average) | Time (Worst) | Space | Notes |
|-----------|----------------|--------------|-------|-------|
| Linear Search | O(n) | O(n) | O(1) | Unsorted data |
| Binary Search | O(log n) | O(log n) | O(1) | Sorted data |
| Hash Lookup | O(1) | O(n) | O(n) | Dictionary/Set |

### Sorting

| Algorithm | Time (Average) | Time (Worst) | Space | Notes |
|-----------|----------------|--------------|-------|-------|
| Timsort (Python) | O(n log n) | O(n log n) | O(n) | `list.sort()`, `sorted()` |
| Quicksort | O(n log n) | O(n²) | O(log n) | In-place |
| Mergesort | O(n log n) | O(n log n) | O(n) | Stable |
| Heapsort | O(n log n) | O(n log n) | O(1) | In-place |
| Bubble Sort | O(n²) | O(n²) | O(1) | Educational only |
| Insertion Sort | O(n²) | O(n²) | O(1) | Small n |

### Graph Algorithms

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| BFS | O(V + E) | O(V) | Breadth-first |
| DFS | O(V + E) | O(V) | Depth-first |
| Dijkstra | O((V + E) log V) | O(V) | Shortest path |
| Topological Sort | O(V + E) | O(V) | DAG ordering |

## Common Problem Complexities

| Problem Type | Typical Complexity | Approach |
|--------------|-------------------|----------|
| Two Sum (hash) | O(n) time, O(n) space | Hash map |
| Two Sum (sorted) | O(n log n) time, O(1) space | Two pointers |
| Sliding Window | O(n) time, O(1) space | Window technique |
| Binary Tree DFS | O(n) time, O(h) space | Recursion/stack |
| Binary Tree BFS | O(n) time, O(w) space | Queue |
| Dynamic Programming | Varies | Memoization/tabulation |

## Space Complexity Guidelines

- **O(1)**: Constant extra space (in-place)
- **O(log n)**: Logarithmic (recursion stack)
- **O(n)**: Linear (copy of input, hash map)
- **O(n²)**: Quadratic (matrix, graph adjacency)

## Quick Reference: Big O Notation

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array access |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Simple loop |
| O(n log n) | Linearithmic | Efficient sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Subsets |
| O(n!) | Factorial | Permutations |

## Tips for Analysis

1. **Drop constants**: O(2n) → O(n)
2. **Drop lower-order terms**: O(n² + n) → O(n²)
3. **Worst-case analysis**: Unless specified otherwise
4. **Space includes**: Input + auxiliary space
5. **Recursion**: Account for call stack space

---

*Last updated: 2024*
