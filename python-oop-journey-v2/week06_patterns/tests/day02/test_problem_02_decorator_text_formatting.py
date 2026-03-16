"""Tests for Problem 02: Decorator Text Formatting."""

from __future__ import annotations

import pytest

from week06_patterns.solutions.day02.problem_02_decorator_text_formatting import (
    TextComponent,
    PlainText,
    TextDecorator,
    BoldDecorator,
    ItalicDecorator,
    UnderlineDecorator,
    ColorDecorator,
    StrikethroughDecorator,
    TextFormatter,
)


class TestPlainText:
    """Tests for the concrete component."""
    
    def test_init(self) -> None:
        text = PlainText("Hello World")
        assert text._text == "Hello World"
    
    def test_render(self) -> None:
        text = PlainText("Hello World")
        assert text.render() == "Hello World"
    
    def test_get_length(self) -> None:
        text = PlainText("Hello")
        assert text.get_length() == 5
    
    def test_empty_text(self) -> None:
        text = PlainText("")
        assert text.render() == ""
        assert text.get_length() == 0


class TestBoldDecorator:
    """Tests for bold decorator."""
    
    def test_implements_interface(self) -> None:
        decorator = BoldDecorator(PlainText("test"))
        assert isinstance(decorator, TextComponent)
        assert isinstance(decorator, TextDecorator)
    
    def test_render_adds_bold_markers(self) -> None:
        decorator = BoldDecorator(PlainText("Hello"))
        assert decorator.render() == "**Hello**"
    
    def test_get_length_returns_raw_length(self) -> None:
        decorator = BoldDecorator(PlainText("Hello"))
        assert decorator.get_length() == 5  # Not including ** markers
    
    def test_nested_decorator(self) -> None:
        decorator = BoldDecorator(ItalicDecorator(PlainText("Hello")))
        result = decorator.render()
        # Bold wraps Italic: results in **\*Hello\*** (Bold outer, Italic inner)
        assert result.startswith("**")
        assert result.endswith("**")
        assert "*Hello*" in result


class TestItalicDecorator:
    """Tests for italic decorator."""
    
    def test_render_adds_italic_markers(self) -> None:
        decorator = ItalicDecorator(PlainText("Hello"))
        assert decorator.render() == "*Hello*"
    
    def test_get_length_returns_raw_length(self) -> None:
        decorator = ItalicDecorator(PlainText("Hello"))
        assert decorator.get_length() == 5


class TestUnderlineDecorator:
    """Tests for underline decorator."""
    
    def test_render_adds_underline_markers(self) -> None:
        decorator = UnderlineDecorator(PlainText("Hello"))
        assert decorator.render() == "__Hello__"
    
    def test_get_length_returns_raw_length(self) -> None:
        decorator = UnderlineDecorator(PlainText("Hello"))
        assert decorator.get_length() == 5


class TestColorDecorator:
    """Tests for color decorator."""
    
    def test_render_adds_color_tags(self) -> None:
        decorator = ColorDecorator(PlainText("Hello"), "red")
        assert decorator.render() == "[color:red]Hello[/color]"
    
    def test_different_colors(self) -> None:
        red = ColorDecorator(PlainText("Hi"), "red")
        blue = ColorDecorator(PlainText("Hi"), "blue")
        
        assert "red" in red.render()
        assert "blue" in blue.render()
    
    def test_get_length_returns_raw_length(self) -> None:
        decorator = ColorDecorator(PlainText("Hello"), "green")
        assert decorator.get_length() == 5
    
    def test_stores_color(self) -> None:
        decorator = ColorDecorator(PlainText("Hello"), "purple")
        assert decorator._color == "purple"


class TestStrikethroughDecorator:
    """Tests for strikethrough decorator."""
    
    def test_render_adds_strikethrough_markers(self) -> None:
        decorator = StrikethroughDecorator(PlainText("Hello"))
        assert decorator.render() == "~~Hello~~"
    
    def test_get_length_returns_raw_length(self) -> None:
        decorator = StrikethroughDecorator(PlainText("Hello"))
        assert decorator.get_length() == 5


class TestDecoratorChaining:
    """Tests for combining multiple decorators."""
    
    def test_bold_italic(self) -> None:
        text = BoldDecorator(ItalicDecorator(PlainText("Hello")))
        result = text.render()
        # Bold wraps Italic: results in **\*Hello\*** (Bold outer, Italic inner)
        assert result.startswith("**")
        assert result.endswith("**")
        assert "*Hello*" in result
    
    def test_multiple_decorators_length_unchanged(self) -> None:
        text = BoldDecorator(ItalicDecorator(UnderlineDecorator(PlainText("Hi"))))
        # Raw text length should still be 2
        assert text.get_length() == 2
    
    def test_all_decorators_together(self) -> None:
        text = ColorDecorator(
            BoldDecorator(
                ItalicDecorator(PlainText("Test"))
            ),
            "blue"
        )
        result = text.render()
        assert result.startswith("[color:blue]")
        assert "**" in result
        assert "*" in result
        assert result.endswith("[/color]")


class TestTextFormatter:
    """Tests for the fluent builder class."""
    
    def test_init(self) -> None:
        formatter = TextFormatter("Hello")
        assert isinstance(formatter._component, PlainText)
    
    def test_bold_returns_self(self) -> None:
        formatter = TextFormatter("Hello")
        result = formatter.bold()
        assert result is formatter
    
    def test_single_format(self) -> None:
        formatter = TextFormatter("Hello").bold()
        assert formatter.render() == "**Hello**"
    
    def test_multiple_formats(self) -> None:
        result = TextFormatter("Hello").bold().italic().render()
        # Order matters: bold applied first, then italic wraps it
        assert "**" in result
        assert "*" in result
        assert "Hello" in result
    
    def test_chaining_all_formats(self) -> None:
        result = (
            TextFormatter("Hello")
            .color("red")
            .bold()
            .underline()
            .render()
        )
        # Last applied wraps first, so underline wraps bold wraps color
        assert "__" in result
        assert "**" in result
        assert "[color:red]" in result
    
    def test_build_returns_component(self) -> None:
        component = TextFormatter("Hello").bold().italic().build()
        # The last applied decorator (italic) wraps the others
        assert isinstance(component, TextComponent)
        assert isinstance(component, ItalicDecorator)
        assert isinstance(component._wrapped, BoldDecorator)
    
    def test_render_convenience(self) -> None:
        formatter = TextFormatter("Test").italic()
        assert formatter.render() == formatter.build().render()
    
    def test_complex_formatting(self) -> None:
        result = (
            TextFormatter("Important")
            .strikethrough()
            .color("gray")
            .render()
        )
        assert result == "[color:gray]~~Important~~[/color]"


class TestDecoratorPolymorphism:
    """Tests demonstrating decorators enable polymorphic use."""
    
    def test_all_components_interchangeable(self) -> None:
        components: list[TextComponent] = [
            PlainText("simple"),
            BoldDecorator(PlainText("bold")),
            ItalicDecorator(BoldDecorator(PlainText("both"))),
            ColorDecorator(PlainText("colored"), "red"),
        ]
        
        results = [c.render() for c in components]
        assert results[0] == "simple"
        assert results[1] == "**bold**"
        assert "colored" in results[3]
    
    def test_client_code_works_with_any_component(self) -> None:
        def format_text(component: TextComponent) -> str:
            return f"Content: {component.render()} (length: {component.get_length()})"
        
        plain = PlainText("Hi")
        decorated = BoldDecorator(ItalicDecorator(PlainText("Hi")))
        
        plain_result = format_text(plain)
        decorated_result = format_text(decorated)
        
        # Both work through same interface
        assert "Content:" in plain_result
        assert "Content:" in decorated_result
        # Both report same raw length
        assert "length: 2" in plain_result
        assert "length: 2" in decorated_result
