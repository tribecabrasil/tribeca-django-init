"""
Entrypoint CLI para o Tribeca Django Init.
Detecta modo MCP (argumentos/flags ou --json) e delega para a interface correta.
Sempre mantenha cli_user.py e cli_mcp.py compatíveis com os mesmos comandos e semântica.
"""

import sys

if __name__ == "__main__":
    # Detecta modo MCP (argumentos/flags ou --json)
    use_json = any(a == "--json" for a in sys.argv)
    # Pode ser expandido para detectar outros sinais de automação/MCP
    if use_json:
        from .cli_mcp import main
    else:
        from .cli_user import main
    main()
