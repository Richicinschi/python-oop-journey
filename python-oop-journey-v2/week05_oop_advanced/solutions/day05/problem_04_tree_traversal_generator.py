"""Reference solution for Problem 04: Tree Traversal Generator."""

from __future__ import annotations
from collections import deque
from typing import Iterator


class TreeNode:
    """A node in a binary tree."""
    
    def __init__(self, value: any, left: TreeNode | None = None, right: TreeNode | None = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def inorder_traversal(root: TreeNode | None) -> Iterator[any]:
    """Generator for inorder traversal (left, root, right)."""
    if root is None:
        return
    yield from inorder_traversal(root.left)
    yield root.value
    yield from inorder_traversal(root.right)


def preorder_traversal(root: TreeNode | None) -> Iterator[any]:
    """Generator for preorder traversal (root, left, right)."""
    if root is None:
        return
    yield root.value
    yield from preorder_traversal(root.left)
    yield from preorder_traversal(root.right)


def postorder_traversal(root: TreeNode | None) -> Iterator[any]:
    """Generator for postorder traversal (left, right, root)."""
    if root is None:
        return
    yield from postorder_traversal(root.left)
    yield from postorder_traversal(root.right)
    yield root.value


def level_order_traversal(root: TreeNode | None) -> Iterator[any]:
    """Generator for level-order (breadth-first) traversal."""
    if root is None:
        return
    
    queue = deque([root])
    while queue:
        node = queue.popleft()
        yield node.value
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


def find_nodes(root: TreeNode | None, predicate: callable) -> Iterator[TreeNode]:
    """Generator to find all nodes matching a predicate."""
    if root is None:
        return
    
    if predicate(root.value):
        yield root
    
    yield from find_nodes(root.left, predicate)
    yield from find_nodes(root.right, predicate)


def tree_depth_generator(root: TreeNode | None, depth: int = 0) -> Iterator[tuple[int, any]]:
    """Generator that yields (depth, value) pairs using level-order traversal."""
    if root is None:
        return
    
    queue = deque([(root, 0)])
    while queue:
        node, d = queue.popleft()
        yield (d, node.value)
        if node.left:
            queue.append((node.left, d + 1))
        if node.right:
            queue.append((node.right, d + 1))
