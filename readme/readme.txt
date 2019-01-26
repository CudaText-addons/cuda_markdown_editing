Plugin for CudaText.
Supports features during editing of Markdown documents.

Symbols *_` (asterisk, underscore, tick)
  - auto-paired on typing
  - if they are typed with selection in editor, selection is enclosed in symbols pair
  - with pair of symbols, BackSpace key - both symbols are deleted
  - with pair of symbols, Space key - right symbol of pair is deleted

Lists (bullet symbols - + * with space)
  - if caret is at the end of non-empty list item, and Enter pressed - newline is added with empty list item (on the same indent as previous item)
  - if caret is at the end of empty list item, and Enter pressed - bullet is deleted and caret goes to bullet position
  - after empty list item, and Tab pressed - list item's indent is increased, and bullet kind is changed (by loop: +-*)
  - after empty list item, and Shift+Tab pressed - list item's indent is decreased, and bullet kind is changed

Tasks
  - [x] foo
    - [x] baz
  - [ ] bim
  if caret is at the end of a task, and Enter pressed - newline with empty unchecked task is added.

Block-quotes
  - if caret at the end of quoted line, and Enter pressed - newline with quote symbol is added
  - if text is selected and > pressed - selection is enclosed in block-quote. First and last lines of multiline selection must not be fully selected. Single line must not be fully selected.

Links
  - if text selected, and ( or [ pressed - selection is enclosed into pair () or []

Crossed text
  - if text selected, and ~ pressed - selection is enclosed like this: ~~text~~

Headers
  - if text selected (single line), and # pressed - # symbol is added in front of selection. If plugin option "match_header_hashes" is on - # symbol mirrors to the end of header. Next # presses will increase header level (##, ###, up to level 6, then # symbols removed).
  - if caret at the and of header, and Enter pressed, and option "match_header_hashes" is on - # symbols are mirrored
  - Setext headers (text with --- or === underline on the next line) - pressing Tab at the end of underline - changes underline length to match the length of header text


Plugin has config file, which you may call via "Options / Settings-plugins / Markdown Editing / Config". Options:
  - list_indent_bullets - allowed bullets (from +-*), for changing bullet kind; for ex, value "-+" means only -+ bullets
  - match_header_hashes - boolean, 0/1 - allows to mirror leading # symbols to the end of header


Author: Medvosa, https://github.com/medvosa
License: MIT
