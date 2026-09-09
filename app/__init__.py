"""Portfolio site for Naveen Mandava — AI/ML Engineer.

The whole site is server rendered from typed Python data:

    app.models    -- dataclasses describing every piece of content
    app.content   -- the actual resume content, as Python objects
    app.charts    -- pure-Python geometry for the SVG charts
    app.main      -- the FastAPI application

Templates under ``app/templates`` only lay out what these modules produce.
"""

__version__ = "1.0.0"
