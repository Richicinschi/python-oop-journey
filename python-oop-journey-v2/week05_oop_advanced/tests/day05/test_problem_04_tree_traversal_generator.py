"""Tests for Problem 04: Tree Traversal Generator."""

from __future__ import annotations

import pytest

from week05_oop_advanced.solutions.day05.problem_04_tree_traversal_generator import (
    TreeNode, inorder_traversal, preorder_traversal, postorder_traversal,
    level_order_traversal, find_nodes, tree_depth_generator
)


@pytest.fixture
def sample_tree() -> TreeNode:
    """Create a sample binary tree:
           1
          / \
         2   3
        / \   \
       4   5   6
    """
    return TreeNode(
        1,
        TreeNode(2, TreeNode(4), TreeNode(5)),
        TreeNode(3, None, TreeNode(6))
    )


@pytest.fixture
def single_node_tree() -> TreeNode:
    """Create a tree with single node."""
    return TreeNode(42)


@pytest.fixture
def empty_tree() -> None:
    """Return None representing empty tree."""
    return None


class TestTreeNode:
    """Tests for TreeNode class."""
    
    def test_tree_node_creation(self) -> None:
        node = TreeNode(5)
        assert node.value == 5
        assert node.left is None
        assert node.right is None
    
    def test_tree_node_with_children(self) -> None:
        left = TreeNode(2)
        right = TreeNode(3)
        root = TreeNode(1, left, right)
        assert root.value == 1
        assert root.left is left
        assert root.right is right


class TestInorderTraversal:
    """Tests for inorder_traversal generator."""
    
    def test_inorder_sample_tree(self, sample_tree: TreeNode) -> None:
        result = list(inorder_traversal(sample_tree))
        assert result == [4, 2, 5, 1, 3, 6]
    
    def test_inorder_single_node(self, single_node_tree: TreeNode) -> None:
        result = list(inorder_traversal(single_node_tree))
        assert result == [42]
    
    def test_inorder_empty(self, empty_tree: None) -> None:
        result = list(inorder_traversal(empty_tree))
        assert result == []


class TestPreorderTraversal:
    """Tests for preorder_traversal generator."""
    
    def test_preorder_sample_tree(self, sample_tree: TreeNode) -> None:
        result = list(preorder_traversal(sample_tree))
        assert result == [1, 2, 4, 5, 3, 6]
    
    def test_preorder_single_node(self, single_node_tree: TreeNode) -> None:
        result = list(preorder_traversal(single_node_tree))
        assert result == [42]
    
    def test_preorder_empty(self, empty_tree: None) -> None:
        result = list(preorder_traversal(empty_tree))
        assert result == []


class TestPostorderTraversal:
    """Tests for postorder_traversal generator."""
    
    def test_postorder_sample_tree(self, sample_tree: TreeNode) -> None:
        result = list(postorder_traversal(sample_tree))
        assert result == [4, 5, 2, 6, 3, 1]
    
    def test_postorder_single_node(self, single_node_tree: TreeNode) -> None:
        result = list(postorder_traversal(single_node_tree))
        assert result == [42]
    
    def test_postorder_empty(self, empty_tree: None) -> None:
        result = list(postorder_traversal(empty_tree))
        assert result == []


class TestLevelOrderTraversal:
    """Tests for level_order_traversal generator."""
    
    def test_level_order_sample_tree(self, sample_tree: TreeNode) -> None:
        result = list(level_order_traversal(sample_tree))
        assert result == [1, 2, 3, 4, 5, 6]
    
    def test_level_order_single_node(self, single_node_tree: TreeNode) -> None:
        result = list(level_order_traversal(single_node_tree))
        assert result == [42]
    
    def test_level_order_empty(self, empty_tree: None) -> None:
        result = list(level_order_traversal(empty_tree))
        assert result == []
    
    def test_level_order_deeper_tree(self) -> None:
        """Test with an unbalanced tree."""
        tree = TreeNode(
            1,
            TreeNode(2, TreeNode(3, TreeNode(4)), None),
            None
        )
        result = list(level_order_traversal(tree))
        assert result == [1, 2, 3, 4]


class TestFindNodes:
    """Tests for find_nodes generator."""
    
    def test_find_nodes_matching(self, sample_tree: TreeNode) -> None:
        result = list(find_nodes(sample_tree, lambda x: x > 3))
        values = [node.value for node in result]
        assert values == [4, 5, 6]
    
    def test_find_nodes_no_matches(self, sample_tree: TreeNode) -> None:
        result = list(find_nodes(sample_tree, lambda x: x > 10))
        assert result == []
    
    def test_find_nodes_single_match(self, sample_tree: TreeNode) -> None:
        result = list(find_nodes(sample_tree, lambda x: x == 1))
        assert len(result) == 1
        assert result[0].value == 1
    
    def test_find_nodes_empty(self, empty_tree: None) -> None:
        result = list(find_nodes(empty_tree, lambda x: True))
        assert result == []
    
    def test_find_nodes_returns_nodes_not_values(self, sample_tree: TreeNode) -> None:
        result = list(find_nodes(sample_tree, lambda x: x == 2))
        assert len(result) == 1
        assert isinstance(result[0], TreeNode)
        assert result[0].left is not None  # Can traverse from found node


class TestTreeDepthGenerator:
    """Tests for tree_depth_generator."""
    
    def test_depth_generator_sample_tree(self, sample_tree: TreeNode) -> None:
        result = list(tree_depth_generator(sample_tree))
        expected = [
            (0, 1),  # root
            (1, 2), (1, 3),  # level 1
            (2, 4), (2, 5), (2, 6)  # level 2
        ]
        assert result == expected
    
    def test_depth_generator_single_node(self, single_node_tree: TreeNode) -> None:
        result = list(tree_depth_generator(single_node_tree))
        assert result == [(0, 42)]
    
    def test_depth_generator_empty(self, empty_tree: None) -> None:
        result = list(tree_depth_generator(empty_tree))
        assert result == []
    
    def test_depth_generator_deeper_tree(self) -> None:
        tree = TreeNode(
            1,
            TreeNode(2, TreeNode(3, TreeNode(4)), None),
            None
        )
        result = list(tree_depth_generator(tree))
        expected = [(0, 1), (1, 2), (2, 3), (3, 4)]
        assert result == expected


class TestGeneratorLazyEvaluation:
    """Tests that verify lazy evaluation of generators."""
    
    def test_inorder_is_generator(self, sample_tree: TreeNode) -> None:
        result = inorder_traversal(sample_tree)
        assert hasattr(result, '__iter__')
        assert hasattr(result, '__next__')
    
    def test_can_iterate_partially(self, sample_tree: TreeNode) -> None:
        gen = inorder_traversal(sample_tree)
        first = next(gen)
        second = next(gen)
        assert first == 4
        assert second == 2
        # Don't consume rest - that's lazy evaluation
    
    def test_level_order_generator_type(self, sample_tree: TreeNode) -> None:
        result = level_order_traversal(sample_tree)
        # Should be a generator, not a list
        assert not isinstance(result, list)
