import re
from typing import List, Optional


def get_content_between_tags(html: str, tag_name: str) -> List[str]:
    """
    Extract all content between HTML tags with the given tag name.

    Args:
        html: The HTML string to search
        tag_name: The name of the tag (e.g., 'div', 'p', 'span')

    Returns:
        A list of strings containing the content between all matching tags

    Examples:
        >>> html = '<div>Hello</div><div>World</div>'
        >>> get_content_between_tags(html, 'div')
        ['Hello', 'World']

        >>> html = '<p>First paragraph</p><span>Some text</span><p>Second paragraph</p>'
        >>> get_content_between_tags(html, 'p')
        ['First paragraph', 'Second paragraph']
    """
    # Create a regex pattern to match opening and closing tags with content
    # This pattern handles nested tags by using non-greedy matching
    pattern = f'<{tag_name}[^>]*>(.*?)</{tag_name}>'

    # Find all matches (re.DOTALL allows . to match newlines)
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

    return matches


def get_first_content_between_tags(html: str, tag_name: str) -> Optional[str]:
    """
    Extract the first occurrence of content between HTML tags with the given tag name.

    Args:
        html: The HTML string to search
        tag_name: The name of the tag (e.g., 'div', 'p', 'span')

    Returns:
        The content between the first matching tags, or None if no match found

    Examples:
        >>> html = '<div>Hello</div><div>World</div>'
        >>> get_first_content_between_tags(html, 'div')
        'Hello'
    """
    matches = get_content_between_tags(html, tag_name)
    return matches[0] if matches else ''


if __name__ == "__main__":
    # Test examples
    test_html = """
    <div>First div</div>
    <p>A paragraph</p>
    <div>Second div with <span>nested span</span></div>
    <span>A span element</span>
    """

    print("All div contents:", get_content_between_tags(test_html, 'div'))
    print("All p contents:", get_content_between_tags(test_html, 'p'))
    print("All span contents:", get_content_between_tags(test_html, 'span'))
    print("First div:", get_first_content_between_tags(test_html, 'div'))
