"""One-Star Review of Something Essential.

Writes one deadpan one-star review of the sun -- an everyday essential
everyone relies on -- to <MAKEFUN_OUTPUT_DIR>/entry.txt (default
/output/entry.txt). Single line, at most 160 characters, no trailing
newline.

The review:

    One star. The sun works one shift a day, takes every weekend off,
    and still expects applause for showing up. Would not recommend as
    a light source.

Why this line (reasoning, kept here and in the README; the entry
itself is just the review):

* Unmistakably a one-star review of an everyday essential: it opens
  "One star." and names the sun, then files a real complaint against
  a thing that cannot be fixed.
* Sharpest true grievance: the sun's schedule. Everyone has cursed
  the short winter day and the sun setting at 5 p.m.; nobody has seen
  it written down as a labour complaint.
* Deadpan throughout: no winking, no exclamation marks, no
  explaining the joke. It reads like an earnest customer review.
* Turns in the last few words: "Would not recommend as a light
  source" -- the sting arrives after the complaint has been read
  straight, and it reframes the sun as a failing product.
* Tight and specific: one shift, every weekend off, applause for
  showing up -- three concrete charges, no filler.

Candidates weighed and set aside: a gravity review ("keeps dropping
everything I own, zero stars for customer service") -- funny, but
the grievance is generic clumsiness, not gravity's own fault;
a Mondays review -- Mondays are a calendar artefact, less essential
than the sun; a sleep review ("arrives late, leaves early, charges
eight hours for four") -- strong, but the sun's one-shift joke turns
harder at the end.

Standard library only. Deterministic: no randomness, no network, no
clock.
"""

import hashlib
import os

TEXT = (
    "One star. The sun works one shift a day, takes every weekend off, "
    "and still expects applause for showing up. "
    "Would not recommend as a light source."
)

MAX_CHARS = 160

# sha256 of the exact bytes main.py must write to entry.txt, measured
# from a verified run. The read-back step asserts the file's digest
# equals this value, so any drift in the written bytes fails loudly.
EXPECTED_SHA256 = (
    "969205593157eafa38c6fb9e17f24ee6e65cba4cbd06c610a5dcc047b5cae704"
)


def validate_text(value) -> str:
    """Guard: value must be a single non-blank line of 1..160 chars.

    Accepts either the text string or the raw bytes read back from the
    entry file, so the same check covers the pre-write guard and the
    post-write read-back verification. Returns the text as a str, or
    raises AssertionError with a clear message.
    """
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    assert 1 <= len(value) <= MAX_CHARS, (
        f"entry.txt must be 1..{MAX_CHARS} characters, got {len(value)}"
    )
    assert value.strip(), "entry.txt must not be only whitespace"
    assert "\n" not in value and "\r" not in value, (
        "entry.txt must be a single line"
    )
    return value


def main() -> None:
    # Pre-write guard: refuse to write anything outside the gate.
    validate_text(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)
    # Read-back validation: the gate is 1..160 characters, so the file
    # must hold exactly the text we intended to write.
    with open(path, "rb") as f:
        data = f.read()
    assert validate_text(data) == TEXT
    # Digest verification: the written bytes must hash to the digest
    # measured from the verified run, proving no drift or stray bytes.
    digest = hashlib.sha256(data).hexdigest()
    assert digest == EXPECTED_SHA256, (
        f"entry.txt sha256 mismatch: got {digest}, "
        f"expected {EXPECTED_SHA256}"
    )
    print(TEXT)
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
