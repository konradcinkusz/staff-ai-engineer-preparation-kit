"""Shared parsing for the gates. Stdlib only.

The balanced-brace reader below is the load-bearing part, and it exists
because of a specific defect rather than out of tidiness.

\\reported{text}{key} takes prose as its first argument, and that prose
contains braces: \\code{...}, \\emph{...}, \\ref{...}. A regex with one level
of nesting reads such a call wrongly -- it stops at the first closing brace it
understands and takes the wrong span as the source key. It does not error. It
silently checks the wrong thing, and a gate that silently checks the wrong
thing is worse than no gate, because it is trusted.

So arguments are read by counting braces, which makes the wrong match
impossible rather than unlikely.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def strip_comments(text: str) -> str:
    """Remove LaTeX comments, respecting \\%.

    A gate that reads commented-out text reports defects nobody can see on the
    page, and the author then deletes the explanation rather than the defect.
    """
    out = []
    for line in text.split("\n"):
        i, escaped = 0, False
        while i < len(line):
            c = line[i]
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == "%":
                line = line[:i]
                break
            i += 1
        out.append(line)
    return "\n".join(out)


def balanced(text: str, start: int) -> tuple[str, int] | None:
    """Read one brace-delimited argument starting at `start`.

    Returns (contents, index just past the closing brace), or None if `start`
    is not an opening brace or the braces never close.
    """
    if start >= len(text) or text[start] != "{":
        return None
    depth, i, escaped = 0, start, False
    while i < len(text):
        c = text[i]
        if escaped:
            escaped = False
        elif c == "\\":
            escaped = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
        i += 1
    return None


def find_calls(text: str, macro: str, args: int, optional: bool = False):
    """Yield (line_number, optional_arg_or_None, [arguments]) for each call.

    Line numbers are 1-based and count from the original text, so a failure
    message can name a line somebody can open.
    """
    needle = "\\" + macro
    i = 0
    while True:
        i = text.find(needle, i)
        if i == -1:
            return
        after = i + len(needle)
        # \reportedly must not match \reported
        if after < len(text) and (text[after].isalpha() or text[after] == "*"):
            i = after
            continue
        line = text.count("\n", 0, i) + 1
        j = after
        opt = None
        if optional and j < len(text) and text[j] == "[":
            close = text.find("]", j)
            if close != -1:
                opt = text[j + 1 : close]
                j = close + 1
        collected, ok = [], True
        for _ in range(args):
            while j < len(text) and text[j] in " \n\t":
                j += 1
            read = balanced(text, j)
            if read is None:
                ok = False
                break
            collected.append(read[0])
            j = read[1]
        if ok:
            yield line, opt, collected
        i = after


def chapter_files() -> list[pathlib.Path]:
    return sorted((ROOT / "chapters").glob("*.tex"))


def prose_files() -> list[pathlib.Path]:
    return chapter_files() + sorted((ROOT / "frontmatter").glob("*.tex"))


def report(name: str, failures: list[str], summary: str) -> int:
    if failures:
        print(f"FAIL [{name}]", flush=True)
        for f in failures:
            print(f"  {f}")
        print(f"\n{len(failures)} failure(s).")
        return 1
    print(f"ok [{name}] {summary}")
    return 0
