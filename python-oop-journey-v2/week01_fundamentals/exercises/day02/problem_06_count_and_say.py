"""Problem 06: Count and Say

Topic: Strings
Difficulty: Medium

The count-and-say sequence is a sequence of digit strings defined by the recursive formula:

- count_and_say(1) = "1"
- count_and_say(n) is the way you would "say" the digit string from count_and_say(n-1),
  which is then converted into a different digit string.

To determine how you "say" a digit string, split it into the minimal number of groups
so that each group is a contiguous section all of the same character. Then for each group,
say the number of characters, then say the character. To convert the saying into a digit string,
replace the counts with a number and concatenate every saying.

For example, the saying and conversion for digit string "3322251":
Given "3322251"
Two 3's, three 2's, one 5, and one 1
=> "23" + "32" + "15" + "11" => "23321511"
"""

from __future__ import annotations


def count_and_say(n: int) -> str:
    """Return the nth term of the count-and-say sequence.
    
    Args:
        n: The term number (1-indexed).
        
    Returns:
        The nth term as a string.
        
    Examples:
        >>> count_and_say(1)
        '1'
        >>> count_and_say(4)
        '1211'
        >>> count_and_say(5)
        '111221'
        
    Note:
        Sequence: 1, 11, 21, 1211, 111221, 312211, ...
    """
    raise NotImplementedError("Implement count_and_say")
