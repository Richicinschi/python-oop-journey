"""Tests for Problem 03: Composite File Tree."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day02.problem_03_composite_file_tree import (
    FileSystemComponent,
    File,
    Directory,
    FileSystemBuilder,
    create_sample_file_system,
)


class TestFile:
    """Tests for the leaf class."""
    
    def test_init(self) -> None:
        file = File("test.txt", 100)
        assert file.name == "test.txt"
        assert file.size == 100
    
    def test_name_property(self) -> None:
        file = File("document.pdf", 2048)
        assert file.name == "document.pdf"
    
    def test_size_property(self) -> None:
        file = File("large.bin", 1000000)
        assert file.size == 1000000
    
    def test_created_property(self) -> None:
        from datetime import datetime
        now = datetime.now()
        file = File("test.txt", 100, now)
        assert file.created == now
    
    def test_default_created(self) -> None:
        file = File("test.txt", 100)
        assert isinstance(file.created, type(__import__('datetime').datetime.now()))
    
    def test_display(self) -> None:
        file = File("test.txt", 100)
        assert file.display() == "[FILE] test.txt (100 bytes)"
    
    def test_display_with_indent(self) -> None:
        file = File("test.txt", 100)
        assert file.display(1) == "  [FILE] test.txt (100 bytes)"
        assert file.display(2) == "    [FILE] test.txt (100 bytes)"
    
    def test_search_match(self) -> None:
        file = File("document.txt", 100)
        assert file.search("doc") == ["document.txt"]
    
    def test_search_case_insensitive(self) -> None:
        file = File("Document.TXT", 100)
        assert file.search("DOC") == ["Document.TXT"]
    
    def test_search_no_match(self) -> None:
        file = File("test.txt", 100)
        assert file.search("xyz") == []


class TestDirectory:
    """Tests for the composite class."""
    
    def test_init(self) -> None:
        dir = Directory("myfolder")
        assert dir.name == "myfolder"
    
    def test_empty_directory_size(self) -> None:
        dir = Directory("empty")
        assert dir.size == 0
    
    def test_directory_with_files_size(self) -> None:
        dir = Directory("folder")
        dir.add(File("a.txt", 100))
        dir.add(File("b.txt", 200))
        assert dir.size == 300
    
    def test_add_file(self) -> None:
        dir = Directory("folder")
        file = File("test.txt", 100)
        dir.add(file)
        assert len(dir.get_children()) == 1
    
    def test_add_directory(self) -> None:
        parent = Directory("parent")
        child = Directory("child")
        parent.add(child)
        assert len(parent.get_children()) == 1
    
    def test_remove_child(self) -> None:
        dir = Directory("folder")
        file = File("test.txt", 100)
        dir.add(file)
        dir.remove(file)
        assert len(dir.get_children()) == 0
    
    def test_remove_nonexistent(self) -> None:
        dir = Directory("folder")
        file = File("test.txt", 100)
        # Should not raise
        dir.remove(file)
    
    def test_get_children_returns_copy(self) -> None:
        dir = Directory("folder")
        dir.add(File("test.txt", 100))
        children = dir.get_children()
        children.clear()
        assert len(dir.get_children()) == 1  # Original unchanged
    
    def test_display_empty(self) -> None:
        dir = Directory("empty")
        assert dir.display() == "[DIR] empty/"
    
    def test_display_with_children(self) -> None:
        dir = Directory("parent")
        dir.add(File("child.txt", 100))
        display = dir.display()
        assert "[DIR] parent/" in display
        assert "[FILE] child.txt" in display
    
    def test_display_nested(self) -> None:
        root = Directory("root")
        sub = Directory("sub")
        sub.add(File("deep.txt", 50))
        root.add(sub)
        
        display = root.display()
        lines = display.split("\n")
        assert lines[0] == "[DIR] root/"
        assert lines[1] == "  [DIR] sub/"
        assert lines[2] == "    [FILE] deep.txt (50 bytes)"
    
    def test_search_in_directory(self) -> None:
        dir = Directory("folder")
        dir.add(File("document.txt", 100))
        dir.add(File("other.pdf", 200))
        
        results = dir.search("doc")
        assert "document.txt" in results
    
    def test_count_files_empty(self) -> None:
        dir = Directory("empty")
        assert dir.count_files() == 0
    
    def test_count_files_single(self) -> None:
        dir = Directory("folder")
        dir.add(File("a.txt", 100))
        assert dir.count_files() == 1
    
    def test_count_files_nested(self) -> None:
        root = Directory("root")
        sub = Directory("sub")
        sub.add(File("a.txt", 100))
        sub.add(File("b.txt", 200))
        root.add(sub)
        root.add(File("c.txt", 300))
        
        assert root.count_files() == 3
    
    def test_count_directories(self) -> None:
        root = Directory("root")
        sub1 = Directory("sub1")
        sub2 = Directory("sub2")
        sub1.add(sub2)
        root.add(sub1)
        
        # root, sub1, sub2 = 3 directories
        assert root.count_directories() == 3


class TestCompositeBehavior:
    """Tests demonstrating composite pattern behavior."""
    
    def test_uniform_interface(self) -> None:
        """Both files and directories implement same interface."""
        components: list[FileSystemComponent] = [
            File("file.txt", 100),
            Directory("folder")
        ]
        
        # Can call same methods on both
        for c in components:
            assert c.name is not None
            assert isinstance(c.size, int)
            assert isinstance(c.display(), str)
    
    def test_nested_size_calculation(self) -> None:
        """Directory size includes all nested children."""
        root = Directory("root")
        level1 = Directory("level1")
        level2 = Directory("level2")
        
        level2.add(File("deep.txt", 50))
        level1.add(level2)
        level1.add(File("mid.txt", 100))
        root.add(level1)
        root.add(File("top.txt", 25))
        
        assert root.size == 175  # 50 + 100 + 25
        assert level1.size == 150  # 50 + 100
        assert level2.size == 50
    
    def test_recursive_search(self) -> None:
        """Search finds matches at any depth."""
        root = Directory("root")
        docs = Directory("documents")
        pics = Directory("pictures")
        
        docs.add(File("report.txt", 100))
        pics.add(File("photo.txt.jpg", 200))
        root.add(docs)
        root.add(pics)
        
        results = root.search(".txt")
        assert "report.txt" in results
        assert "documents" not in results  # Directory doesn't have .txt


class TestFileSystemBuilder:
    """Tests for the builder utility."""
    
    def test_init(self) -> None:
        builder = FileSystemBuilder("myroot")
        root = builder.build()
        assert root.name == "myroot"
    
    def test_add_file_at_root(self) -> None:
        builder = FileSystemBuilder()
        builder.add_file("test.txt", 100)
        root = builder.build()
        
        assert len(root.get_children()) == 1
        assert root.get_children()[0].name == "test.txt"
    
    def test_add_file_in_subdir(self) -> None:
        builder = FileSystemBuilder()
        builder.add_file("docs/report.txt", 500)
        root = builder.build()
        
        # Should have created docs directory
        docs = root.get_children()[0]
        assert isinstance(docs, Directory)
        assert docs.name == "docs"
        assert docs.get_children()[0].name == "report.txt"
    
    def test_add_multiple_files_same_dir(self) -> None:
        builder = FileSystemBuilder()
        builder.add_file("docs/a.txt", 100).add_file("docs/b.txt", 200)
        root = builder.build()
        
        docs = root.get_children()[0]
        assert len(docs.get_children()) == 2
    
    def test_chaining(self) -> None:
        builder = FileSystemBuilder()
        result = builder.add_file("a.txt", 100)
        assert result is builder  # Returns self


class TestSampleFileSystem:
    """Tests for the sample file system factory."""
    
    def test_structure(self) -> None:
        root = create_sample_file_system()
        
        assert root.name == "root"
        assert root.count_directories() == 4  # root, documents, photos, vacation
        # resume.pdf, cover_letter.txt, beach.jpg, mountain.jpg, portrait.png, readme.txt = 6 files
        assert root.count_files() == 6
    
    def test_total_size(self) -> None:
        root = create_sample_file_system()
        # 4500 + 1200 + 2048 + 3072 + 1536 + 512 = 12868
        assert root.size == 12868
    
    def test_documents_contents(self) -> None:
        root = create_sample_file_system()
        
        docs = None
        for child in root.get_children():
            if child.name == "documents":
                docs = child
                break
        
        assert docs is not None
        assert isinstance(docs, Directory)
        assert docs.count_files() == 2
    
    def test_search_pdf(self) -> None:
        root = create_sample_file_system()
        results = root.search(".pdf")
        assert "resume.pdf" in results
    
    def test_search_jpg(self) -> None:
        root = create_sample_file_system()
        results = root.search(".jpg")
        assert "beach.jpg" in results
        assert "mountain.jpg" in results
    
    def test_display_output(self) -> None:
        root = create_sample_file_system()
        display = root.display()
        
        assert "[DIR] root/" in display
        assert "[DIR] documents/" in display
        assert "[FILE] resume.pdf" in display
        assert "(4500 bytes)" in display
