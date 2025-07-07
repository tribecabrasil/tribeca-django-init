"""Entry point for the Tribeca Django Init CLI.

The module detects whether automation (MCP) mode is requested via the
``--json`` flag and delegates to the appropriate interface. Keep
``cli_user.py`` and ``cli_mcp.py`` synchronized so they support the same
commands and semantics.
"""
import sys

if __name__ == "__main__":
    # Detect MCP mode (arguments/flags or --json)
    use_json = any(a == "--json" for a in sys.argv)
    # This can be expanded to detect other automation signals
    if use_json:
        from .cli_mcp import main
    else:
        from .cli_user import main
    main()

