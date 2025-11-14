from fastmcp import FastMCP
from typing import Literal


mcp = FastMCP("hello-mcp-server")

@mcp.tool()
def greet_person(
    name: str,
    lang: Literal["ja", "en"] = "ja"
) -> str:
    """
    名前を指定すると、その人に挨拶を返します。
    - ユーザーが「挨拶」「hello」「greet」などと入力した場合に利用されます。
    - lang="ja" で日本語、lang="en" で英語の挨拶を返します。
    """

    if lang == "en":
        return f"Hello, {name}! Welcome to the Hello World MCP server!"
    return f"こんにちは、{name}さん！\nHello World MCPサーバーへようこそ！"


if __name__ == "__main__":
    mcp.run()
