"""Tests for Problem 04: Batched Repository."""

from __future__ import annotations

from week07_real_world.solutions.day06.problem_04_batched_repository import (
    BatchedRepository,
    BufferedWriter,
    ChunkedProcessor,
)


def test_batched_repository_add_and_get() -> None:
    """Test basic add and get operations."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=10)
    repo.add("item1", 1)
    assert repo.get(1) == "item1"


def test_batched_repository_pending_count() -> None:
    """Test pending count tracking."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=10)
    assert repo.pending_count == 0
    
    repo.add("item1", 1)
    assert repo.pending_count == 1
    
    repo.add("item2", 2)
    assert repo.pending_count == 2


def test_batched_repository_is_dirty() -> None:
    """Test is_dirty property."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=10)
    assert not repo.is_dirty
    
    repo.add("item1", 1)
    assert repo.is_dirty
    
    repo.flush()
    assert not repo.is_dirty


def test_batched_repository_flush() -> None:
    """Test flush executes pending operations."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=10)
    repo.add("item1", 1)
    repo.add("item2", 2)
    
    result = repo.flush()
    assert result == {'added': 2, 'deleted': 0}
    assert repo.pending_count == 0
    
    # Data should still be accessible
    assert repo.get(1) == "item1"
    assert repo.get(2) == "item2"


def test_batched_repository_delete() -> None:
    """Test delete operation."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=10)
    repo.add("item1", 1)
    repo.flush()
    
    repo.delete(1)
    assert repo.pending_count == 1
    assert repo.get(1) is None  # Should be None due to pending delete
    
    repo.flush()
    assert repo.get(1) is None


def test_batched_repository_delete_pending_add() -> None:
    """Test deleting an item that was added but not flushed."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=10)
    repo.add("item1", 1)
    repo.delete(1)
    
    # Item should not be accessible (deleted)
    assert repo.get(1) is None
    # Should be marked as deleted (operation still pending)
    assert 1 in repo._pending_deletes


def test_batched_repository_add_after_delete() -> None:
    """Test adding an item that was marked for deletion."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=10)
    repo.add("item1", 1)
    repo.flush()
    
    repo.delete(1)
    repo.add("item1_new", 1)
    
    assert repo.get(1) == "item1_new"
    assert repo.pending_count == 1  # Only add, delete was removed


def test_batched_repository_auto_flush() -> None:
    """Test auto-flush when batch size is reached."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=3)
    
    repo.add("item1", 1)
    repo.add("item2", 2)
    assert repo.pending_count == 2
    
    repo.add("item3", 3)  # Should trigger auto-flush
    assert repo.pending_count == 0


def test_batched_repository_close() -> None:
    """Test close flushes remaining operations."""
    repo: BatchedRepository[str, int] = BatchedRepository(batch_size=10)
    repo.add("item1", 1)
    repo.add("item2", 2)
    
    repo.close()
    assert repo.pending_count == 0
    assert repo.get(1) == "item1"
    assert repo.get(2) == "item2"


def test_buffered_writer_init() -> None:
    """Test BufferedWriter initialization."""
    writer = BufferedWriter(batch_size=10)
    assert writer.buffer_size == 0
    assert writer.total_written == 0


def test_buffered_writer_write() -> None:
    """Test write adds to buffer."""
    writer = BufferedWriter(batch_size=10)
    writer.write("item1")
    writer.write("item2")
    
    assert writer.buffer_size == 2
    assert writer.total_written == 0  # Not flushed yet


def test_buffered_writer_auto_flush() -> None:
    """Test auto-flush when batch size is reached."""
    writer = BufferedWriter(batch_size=3)
    
    writer.write("item1")
    writer.write("item2")
    assert writer.buffer_size == 2
    
    writer.write("item3")  # Should trigger auto-flush
    assert writer.buffer_size == 0
    assert writer.total_written == 3


def test_buffered_writer_manual_flush() -> None:
    """Test manual flush."""
    writer = BufferedWriter(batch_size=10)
    writer.write("item1")
    writer.write("item2")
    
    count = writer.flush()
    assert count == 2
    assert writer.buffer_size == 0
    assert writer.total_written == 2


def test_buffered_writer_flush_empty() -> None:
    """Test flush with empty buffer."""
    writer = BufferedWriter(batch_size=10)
    count = writer.flush()
    assert count == 0


def test_buffered_writer_total_written_accumulates() -> None:
    """Test total_written accumulates across multiple flushes."""
    writer = BufferedWriter(batch_size=2)
    
    writer.write("item1")
    writer.write("item2")  # Auto-flush
    assert writer.total_written == 2
    
    writer.write("item3")
    writer.write("item4")  # Auto-flush
    assert writer.total_written == 4


def test_buffered_writer_close() -> None:
    """Test close flushes remaining items."""
    writer = BufferedWriter(batch_size=10)
    writer.write("item1")
    writer.write("item2")
    
    writer.close()
    assert writer.buffer_size == 0
    assert writer.total_written == 2


def test_buffered_writer_closed_raises() -> None:
    """Test writing to closed writer raises error."""
    writer = BufferedWriter(batch_size=10)
    writer.write("item1")
    writer.close()
    
    try:
        writer.write("item2")
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass


def test_chunked_processor_init() -> None:
    """Test ChunkedProcessor initialization."""
    processor: ChunkedProcessor[int] = ChunkedProcessor(chunk_size=5)
    assert processor.current_chunk_size == 0


def test_chunked_processor_add() -> None:
    """Test add accumulates items."""
    processor: ChunkedProcessor[int] = ChunkedProcessor(chunk_size=5)
    
    result = processor.add(1)
    assert result is None
    assert processor.current_chunk_size == 1


def test_chunked_processor_add_returns_full_chunk() -> None:
    """Test add returns chunk when full."""
    processor: ChunkedProcessor[int] = ChunkedProcessor(chunk_size=3)
    
    processor.add(1)
    processor.add(2)
    result = processor.add(3)
    
    assert result == [1, 2, 3]
    assert processor.current_chunk_size == 0


def test_chunked_processor_finalize() -> None:
    """Test finalize returns partial chunk."""
    processor: ChunkedProcessor[int] = ChunkedProcessor(chunk_size=5)
    processor.add(1)
    processor.add(2)
    
    result = processor.finalize()
    assert result == [1, 2]


def test_chunked_processor_finalize_empty() -> None:
    """Test finalize returns None when empty."""
    processor: ChunkedProcessor[int] = ChunkedProcessor(chunk_size=5)
    result = processor.finalize()
    assert result is None


def test_chunked_processor_reset() -> None:
    """Test reset clears state."""
    processor: ChunkedProcessor[int] = ChunkedProcessor(chunk_size=5)
    processor.add(1)
    processor.add(2)
    
    processor.reset()
    assert processor.current_chunk_size == 0


def test_chunked_processor_multiple_chunks() -> None:
    """Test processing multiple full chunks."""
    processor: ChunkedProcessor[int] = ChunkedProcessor(chunk_size=2)
    
    chunks = []
    for i in range(7):
        result = processor.add(i)
        if result:
            chunks.append(result)
    
    # Should have 3 full chunks (0,1), (2,3), (4,5)
    assert len(chunks) == 3
    assert chunks[0] == [0, 1]
    assert chunks[1] == [2, 3]
    assert chunks[2] == [4, 5]
    assert processor.current_chunk_size == 1  # 6 is pending


def test_chunked_processor_current_chunk_size() -> None:
    """Test current_chunk_size tracking."""
    processor: ChunkedProcessor[int] = ChunkedProcessor(chunk_size=5)
    
    assert processor.current_chunk_size == 0
    processor.add(1)
    assert processor.current_chunk_size == 1
    processor.add(2)
    assert processor.current_chunk_size == 2
