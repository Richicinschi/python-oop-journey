"""Problem 04: Tree Traversal Generator

Topic: Recursive Generators
Difficulty: Medium

Implement binary tree traversal using generators with yield.
Demonstrates recursive generators and lazy tree iteration.
"""

from __future__ import annotations
from typing import Iterator


class TreeNode:
    """A node in a binary tree.
    
    Attributes:
        value: The value stored in this node
        left: Left child node (or None)
        right: Right child node (or None)
    """
    
    def __init__(self, value: any, left: TreeNode | None = None, right: TreeNode | None = None) -> None:
        """Initialize a tree node.
        
        Args:
            value: The value to store in this node
            left: Left child (default None)
            right: Right child (default None)
        """
        raise NotImplementedError("Implement __init__")


def inorder_traversal(root: TreeNode | None) -> Iterator[any]:
    """Generator for inorder traversal (left, root, right).
    
    Args:
        root: The root node of the tree (or subtree)
        
    Yields:
        Values in inorder sequence
    """
    raise NotImplementedError("Implement inorder_traversal")


def preorder_traversal(root: TreeNode | None) -> Iterator[any]:
    """Generator for preorder traversal (root, left, right).
    
    Args:
        root: The root node of the tree (or subtree)
        
    Yields:
        Values in preorder sequence
    """
    raise NotImplementedError("Implement preorder_traversal")


def postorder_traversal(root: TreeNode | None) -> Iterator[any]:
    """Generator for postorder traversal (left, right, root).
    
    Args:
        root: The root node of the tree (or subtree)
        
    Yields:
        Values in postorder sequence
    """
    raise NotImplementedError("Implement postorder_traversal")


def level_order_traversal(root: TreeNode | None) -> Iterator[any]:
    """Generator for level-order (breadth-first) traversal.
    
    Args:
        root: The root node of the tree (or subtree)
        
    Yields:
        Values level by level, left to right
    """
    raise NotImplementedError("Implement level_order_traversal")


def find_nodes(root: TreeNode | None, predicate: callable) -> Iterator[TreeNode]:
    """Generator to find all nodes matching a predicate.
    
    Args:
        root: The root node to search from
        predicate: Function that takes a value and returns bool
        
    Yields:
        TreeNode objects that satisfy the predicate
    """
    raise NotImplementedError("Implement find_nodes")


def tree_depth_generator(root: TreeNode | None) -> Iterator[tuple[int, any]]:
    """Generator that yields (depth, value) pairs.
    
    Args:
        root: The root node of the tree
        
    Yields:
        Tuples of (depth, value) where depth is 0 for root
    """
    raise NotImplementedError("Implement tree_depth_generator")


# Hints for Tree Traversal Generator (Medium):
# 
# Hint 1 - Conceptual nudge:
# Recursive generators need yield from to delegate to sub-generators.
#
# Hint 2 - Structural plan:
# - Inorder: yield from inorder(left), yield value, yield from inorder(right)
# - Preorder: yield value, then left, then right
# - Postorder: left, right, then yield value
# - Level order: use a queue (collections.deque)
#
# Hint 3 - Edge-case warning:
# Always check if node is None before recursing. For level order, remember to add
# children to the queue even if they're None (or check before adding).
