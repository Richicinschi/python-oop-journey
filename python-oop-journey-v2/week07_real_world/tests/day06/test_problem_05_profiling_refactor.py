"""Tests for Problem 05: Profiling Refactor."""

from __future__ import annotations

from week07_real_world.solutions.day06.problem_05_profiling_refactor import (
    OptimizedDataProcessor,
    ProfileReport,
    SlowDataProcessor,
    profile_operation,
)


def test_slow_fibonacci_base_cases() -> None:
    """Test slow fibonacci base cases."""
    processor = SlowDataProcessor()
    assert processor.slow_fibonacci(0) == 0
    assert processor.slow_fibonacci(1) == 1


def test_slow_fibonacci_small_values() -> None:
    """Test slow fibonacci for small values."""
    processor = SlowDataProcessor()
    assert processor.slow_fibonacci(2) == 1
    assert processor.slow_fibonacci(3) == 2
    assert processor.slow_fibonacci(5) == 5
    assert processor.slow_fibonacci(10) == 55


def test_optimized_fibonacci_base_cases() -> None:
    """Test optimized fibonacci base cases."""
    processor = OptimizedDataProcessor()
    assert processor.fibonacci(0) == 0
    assert processor.fibonacci(1) == 1


def test_optimized_fibonacci_small_values() -> None:
    """Test optimized fibonacci for small values."""
    processor = OptimizedDataProcessor()
    assert processor.fibonacci(2) == 1
    assert processor.fibonacci(3) == 2
    assert processor.fibonacci(5) == 5
    assert processor.fibonacci(10) == 55


def test_optimized_fibonacci_large_value() -> None:
    """Test optimized fibonacci handles larger values efficiently."""
    processor = OptimizedDataProcessor()
    # Should complete quickly with memoization
    result = processor.fibonacci(100)
    assert result == 354224848179261915075


def test_optimized_fibonacci_caching() -> None:
    """Test that fibonacci results are cached."""
    processor = OptimizedDataProcessor()
    
    # Clear and track
    processor.clear_cache()
    initial_hits = processor.get_stats()['cache_hits']
    
    processor.fibonacci(50)
    after_first = processor.get_stats()['cache_hits']
    
    processor.fibonacci(50)  # Should hit cache
    after_second = processor.get_stats()['cache_hits']
    
    # Second call should have resulted in a cache hit
    assert after_second > after_first
    assert processor.get_stats()['cache_hits'] > initial_hits


def test_slow_find_duplicates() -> None:
    """Test slow find_duplicates."""
    processor = SlowDataProcessor()
    items = ['a', 'b', 'c', 'a', 'b', 'd']
    result = processor.find_duplicates(items)
    assert sorted(result) == ['a', 'b']


def test_optimized_find_duplicates() -> None:
    """Test optimized find_duplicates."""
    processor = OptimizedDataProcessor()
    items = ['a', 'b', 'c', 'a', 'b', 'd']
    result = processor.find_duplicates(items)
    assert sorted(result) == ['a', 'b']


def test_find_duplicates_no_duplicates() -> None:
    """Test find_duplicates with no duplicates."""
    slow_processor = SlowDataProcessor()
    fast_processor = OptimizedDataProcessor()
    items = ['a', 'b', 'c', 'd']
    
    assert slow_processor.find_duplicates(items) == []
    assert fast_processor.find_duplicates(items) == []


def test_find_duplicates_all_same() -> None:
    """Test find_duplicates with all items the same."""
    slow_processor = SlowDataProcessor()
    fast_processor = OptimizedDataProcessor()
    items = ['a', 'a', 'a', 'a']
    
    assert slow_processor.find_duplicates(items) == ['a']
    assert fast_processor.find_duplicates(items) == ['a']


def test_find_duplicates_results_match() -> None:
    """Test that both implementations produce same results."""
    slow_processor = SlowDataProcessor()
    fast_processor = OptimizedDataProcessor()
    items = ['x', 'y', 'z', 'x', 'y', 'z', 'w', 'x']
    
    slow_result = sorted(slow_processor.find_duplicates(items))
    fast_result = sorted(fast_processor.find_duplicates(items))
    assert slow_result == fast_result


def test_count_word_frequencies() -> None:
    """Test word frequency counting."""
    slow_processor = SlowDataProcessor()
    fast_processor = OptimizedDataProcessor()
    text = "the quick brown fox jumps over the lazy dog"
    
    slow_result = slow_processor.count_word_frequencies(text)
    fast_result = fast_processor.count_word_frequencies(text)
    
    assert slow_result == fast_result
    assert slow_result['the'] == 2
    assert slow_result['quick'] == 1


def test_count_word_frequencies_caching() -> None:
    """Test that word frequency results are cached."""
    processor = OptimizedDataProcessor()
    text = "hello world hello"
    
    processor.count_word_frequencies(text)
    first_calls = processor.get_stats()['calls']
    
    processor.count_word_frequencies(text)  # Same text
    assert processor.get_stats()['cache_hits'] > 0


def test_count_word_frequencies_case_insensitive() -> None:
    """Test word frequency is case insensitive."""
    processor = OptimizedDataProcessor()
    text = "Hello WORLD hello World"
    result = processor.count_word_frequencies(text)
    
    assert result['hello'] == 2
    assert result['world'] == 2


def test_count_word_frequencies_punctuation() -> None:
    """Test word frequency handles punctuation."""
    processor = OptimizedDataProcessor()
    text = "Hello, world! Hello... world?"
    result = processor.count_word_frequencies(text)
    
    assert result['hello'] == 2
    assert result['world'] == 2


def test_clear_cache() -> None:
    """Test clearing caches."""
    processor = OptimizedDataProcessor()
    processor.fibonacci(10)
    processor.count_word_frequencies("hello world")
    
    assert processor.cache_info['fib_cache_size'] > 0
    
    processor.clear_cache()
    assert processor.cache_info['fib_cache_size'] == 0
    assert processor.cache_info['word_cache_size'] == 0
    assert processor.get_stats()['cache_hits'] == 0


def test_cache_info() -> None:
    """Test cache info reporting."""
    processor = OptimizedDataProcessor()
    processor.fibonacci(5)
    processor.count_word_frequencies("test")
    
    info = processor.cache_info
    assert 'fib_cache_size' in info
    assert 'word_cache_size' in info
    assert 'cache_hits' in info
    assert 'cache_misses' in info
    assert 'hit_rate' in info


def test_profile_report_creation() -> None:
    """Test ProfileReport creation."""
    report = ProfileReport(
        operation='test',
        before_time=10.0,
        after_time=2.0,
        before_result='a',
        after_result='a'
    )
    assert report.operation == 'test'
    assert report.before_time == 10.0
    assert report.after_time == 2.0


def test_profile_report_speedup_factor() -> None:
    """Test speedup calculation."""
    report = ProfileReport(
        operation='test',
        before_time=10.0,
        after_time=2.0,
        before_result='a',
        after_result='a'
    )
    assert report.speedup_factor == 5.0


def test_profile_report_results_match() -> None:
    """Test results match detection."""
    report = ProfileReport(
        operation='test',
        before_time=1.0,
        after_time=0.5,
        before_result=[1, 2, 3],
        after_result=[1, 2, 3]
    )
    assert report.results_match


def test_profile_report_results_differ() -> None:
    """Test results differ detection."""
    report = ProfileReport(
        operation='test',
        before_time=1.0,
        after_time=0.5,
        before_result=[1, 2, 3],
        after_result=[1, 2, 4]
    )
    assert not report.results_match


def test_profile_operation() -> None:
    """Test profile_operation helper function."""
    slow = SlowDataProcessor()
    fast = OptimizedDataProcessor()
    
    report = profile_operation(
        'fibonacci',
        slow,
        fast,
        'slow_fibonacci',
        'fibonacci',
        10
    )
    
    assert report.operation == 'fibonacci'
    assert report.results_match
    assert report.speedup_factor > 0


def test_optimized_is_faster_for_fibonacci() -> None:
    """Verify optimized version is actually faster."""
    slow = SlowDataProcessor()
    fast = OptimizedDataProcessor()
    
    report = profile_operation(
        'fibonacci',
        slow,
        fast,
        'slow_fibonacci',
        'fibonacci',
        15
    )
    
    # Optimized should be significantly faster
    assert report.speedup_factor > 10
