# Bundled fonts

These TrueType fonts are embedded (via `@font-face`) by
`meta_reports.hiv_exit_review_form_report` so the generated PDF renders
identically on every platform, regardless of which fonts happen to be installed
on the host. Without an embedded font, WeasyPrint falls back to a system font
(e.g. DejaVu Sans on Ubuntu) whose taller metrics can push content onto a second
page.

## Liberation Sans

- Family: Liberation Sans (metric-compatible with Arial/Helvetica)
- Faces: Regular, Bold, Italic, Bold Italic
- License: SIL Open Font License, Version 1.1 (OFL-1.1)
- Copyright: Digitized data copyright © 2010 Google Corporation; Liberation is a
  trademark of Red Hat, Inc.
- Upstream: https://github.com/liberationfonts/liberation-fonts

The SIL OFL permits bundling and redistribution with software. See
https://openfontlicense.org/ for the full license text.
