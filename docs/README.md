# Battleship Game Documentation

This folder contains comprehensive API documentation for the battleship game project, generated using Python's built-in `pydoc` tool.

## Documentation Files

- **index.html** - Main documentation index with links to all modules
- **main.html** - Documentation for the main entry point module
- **src.game.html** - Game controller and UI management
- **src.player.html** - Abstract base player class
- **src.human.html** - Human player implementation
- **src.ai.html** - AI player with intelligent targeting
- **src.board.html** - Game board and ship management
- **src.grid.html** - 2D grid foundation class
- **src.utils.html** - Utility classes, enums, and constants

## Viewing the Documentation

To view the documentation:

1. Open `index.html` in a web browser for the main navigation page
2. Or open any individual HTML file directly for specific module documentation

## Generating Documentation

This documentation was generated using:

```bash
python3 -m pydoc -w main
python3 -m pydoc -w src.utils src.player src.human src.ai src.board src.grid src.game
```

The documentation follows Python industry standards with comprehensive docstrings that include:

- Module descriptions
- Class descriptions with attributes
- Method and function descriptions
- Parameter types and descriptions
- Return value descriptions
- Usage examples where appropriate

All docstrings follow Google-style documentation conventions for consistency and readability.