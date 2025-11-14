# Usage MyMCP on VScode
wrote: 2025.11.14

### 要旨
アプリケーション開発にMCPサーバの機能を生かしていきたが、
MCPのセッティングなどに慣れていない＆慣れ親しんだVScodeでの試行を第一歩にしたい人に向けた、
簡易な自作MCPサーバを参考にしたChat対話セッティングの方法をまとめています。

！…
記載者はソフトフェアエンジニアでなく、プロダクトマネージャーのため（予防線）、
記載されている技術的な内容に関し、意図せず不備が含まれている恐れがあります。
不適切な箇所・改善できる箇所があればPRなどを通じご指摘いただければ幸いです。

---

### 1. はじめに
生成AIが外部のツールやデータにアクセスする方法としてMCPが登場※1しています。

MCPの構成要素として、1）MCPホスト、2）MCPクライント、3）MCPサーバがあり、
利用者がツールとして活用する対象が、MCPサーバとなっています。
MCPサーバは様々な組織、団体が開発していますが、個人でもMCPサーバを開発できます。

アプリケーション開発にMCPサーバの機能を生かしていくことをゴールとしたとき、
いくつかのサブプロセスに分解できます。例えば以下のようなサブプロセスが考えられます。
1. 公開されているMPCサーバを対話形式で試す。
2. 自作のMPCサーバを対話形式で試す。
3. 公開されているMPCサーバを自作のアプリケーションに組み込んで利用する。
4. 自作のMPCサーバを自作のアプリケーションに組み込んで利用する。

ここでは「2. 自作のMPCサーバを対話形式で試す。」セッティング方法をまとめます。
また、本セッティング方法の特徴として
**VScodeでの自作のMPCサーバをVScodeでの標準機能となったGitHub Copilot agent modeを用いた対話形式**でこれを実現します。なお、本手順実施においては費用支出はありません。


本手順での前提環境情報一覧は以下です。

| 環境観点       | 今回のセッティング | その他選択肢 | 
| ------------------ | ------------------ | ------------ | 
| OS                 | Windows 11         | Mac          | 
| 開発言語           | Python             | JavaScript   | 
| MCPホスト          | Claude Haiku 4.5   | VScode/GitHub Copilot agent modedにて指定可能なLLM （GPT ***， Geminiなど） | 
| MCPクライント      | VScode / GitHub Copilot agent moded       | Claude for Desktop         | 
| MCPサーバ          | 自作（[試行にあたって参考利用させてもらった"hello-mcp-server" ※2](https://qiita.com/daikumatan/items/1bd7cd532e2de5c7f4cd#21-hello-world-python%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AE%E4%BD%9C%E6%88%90)）          | 公開されているMCPサーバ（["mcp-server-time"](https://github.com/modelcontextprotocol/servers/tree/main/src/time)など）         | 
| MCPサーバ開発フレームワーク | FastMCP         |  EasyMCP，FastAPI-MCP，Template MCPなど       | 

その他前提事項
1. VScodeインストールとMCP設定()※3
2. Githubアカウント取得（VScode/GitHub Copilot agent modedに必要）※4
3. uv(Pythonの仮想環境管理アプリケーション)


### 2. アプローチステップ
### 2.1. 参考情報の確認と修正ポイントの確認
今回の類似した先行試行を調査すると、以下に近しいことを実施されている方と情報があることがわかります。
1. [自作 MCP Server Hands-On Part1: 補足編](https://qiita.com/daikumatan/items/1bd7cd532e2de5c7f4cd#2-fastmcp%E3%81%AB%E3%82%88%E3%82%8Bhello-world-mcp-server-%E3%81%AE%E4%BD%9C%E6%88%90)
2. [MCPというものが流行っているようなので調べたい](https://zenn.dev/kiyuka/scraps/89e9f15197db66#comment-28c257e44a1f8c)
3. [FastMCP での MCPサーバ と MCPクライアント の構築を試す](https://note.com/npaka/n/nce97c892d973)
他に参考情報などを調査

**先行試行 1：**
自作でのMCPサーバ（"hello-mcp-server"）の利用を実施されていることがわかり、
簡易MCPサーバの書き方とそれに必要なライブラリ、MCPサーバとして登録（yaml）が必要なことがわかります。
一方、MCPクライントが VS Code/拡張機能 Continueで実施されていることが違いとなります。
本手順でもこちらの内容をベースに拝借させていただき、実施していきます。

**先行試行 2：**
大まかなMCPサーバ利用のオンボーディングを手順と参考情報を記載しつつ、実施されており、流れを追うことができます。
MCPクライントはClaude desktopで実施され、claude_desktop_config.jsonでMCPサーバへの登録情報を作成しています。
ここから、MCPサーバ登録のファイルは、MCPクライントのアプリケーション依存の可能性があることがわかります。
なお、※6より、VScodeでは.vscode/mcp.jsonでのファイル作成方式があることがわかります。

**先行試行 3：**
大まかなMCPサーバ利用のオンボーディング手順をMCPサーバ開発フレームワークのFastMCP観点から流れを追うことができます。
MCPクライントはCursorで実施されていますが、MCPサーバファイルは、mcp.jsonであることがわかります。
--directoryでの自プロジェクトの絶対パス指定方法例を確認できます。

**簡易まとめ**
- 自作MCPサーバのファイルはpyファイルで作成可能（hello_mcp.py, server.py）
- 自作MCPサーバのpyファイルは、MCPサーバでの機能とサーバ立ち上げ機能を同時に書いていることがこれまで例では多い
- 自作MCPサーバのpyファイルは、Flaskのようなイメージでよい様子（＋サーバとロジックを一緒に書いている状態）
- 自作MCPサーバのpyファイルでは、MCPのライブラリとしてFastMCPを活用
- 自作MCPサーバのpyファイルをターミナルで実行していない → mcp.jsonからのGUIにて`▷Start`している
- MCPサーバのpyとmcp.jsonが最低必要
- MCPサーバのpyは先行試行 1の内容を拝借
- mcp.jsonの書きっぷりは※6を参考としつつ、調整
- 自作MCPサーバをVScode/GitHub Copilot agent modedで利用するには、`📎`でチェックして有効化が必要

→ 以上から、次ステップを以降の章として実施し、
"「佐藤さんに挨拶してください」というユーザ入力に対し、
 「こんにちは、佐藤さん！Hello World MCPサーバーへようこそ！」というレスポンスを
 受け取ること"をゴールに進めていきます。
  
### 2.2. 自作MCPサーバの構築
1. クローンしたワーキングリポジトリにて、uv syncを実施、関連ファイルの自動作成
2. [hello_mcp.py](../hello_mcp.py) ファイル作成・内容記載
3. コマンドプロンプトで`uv run hello_mcp.py`で正常起動として、FASTMCPの画像がターミナルに続けて出力確認（Ctrl+Cで終了）
4. コマンドプロンプトで別のディレクトリに移動 (例　cd ..)
5. コマンドプロンプトで`uv --directory {your working dir has hello_mcp.py} run hello_mcp.py`で出力確認（Ctrl+Cで終了）
（例　uv --directory C:\\MyPrograms\\QuadrantChart run hello_mcp.py）
6. Ctrl+Cで明示的に停止

### 2.3. MCPクライアントでの自作MCPサーバ起動・登録
1. [mcp.json](../.vscode/mcp.json) ファイル作成・内容記載(directoryの指定パスだけ注意)
2. [mcp.json](../.vscode/mcp.json) ファイルで、`▷Start`してMCPサーバを起動
3. Ctrl+Alt+iまたはVScodeの最上部中央検索ボックス右のチャットアイコンから`Open Chat`
4. 展開されたチャット画面下の最左プルダウンを`Agent`に指定、その右手の`📎`をクリック、`hello-mcp-server`をチェックしてMCPサーバを登録

### 2.4. MCP Clientでの自作MCP Serverの起動
1.  チャット画面で、「佐藤さんに挨拶してください」と入力、Enter
2.  実行確認を問われたら適宜`Allow`し、「こんにちは、佐藤さん！
Hello World MCPサーバーへようこそ！」が出力されることを確認


### 3. 振り返り
**VScodeでの自作のMPCサーバをVScodeでの標準機能となったGitHub Copilot agent modeを用いた対話形式**のセッティング方法をまとめられました。
アプリケーション開発へのMCPサーバ活用へ展開するためのベースとしてこれを活用できます。

今後の検討候補は以下が考えられます。
- FastMCPでの通信内容の確認（kwd. MCP Inspector）
- MCPサーバを利用したアプリケーション開発
- MCPサーバ環境のコンテナ化
- MCPサーバの公開（kwd. Time MCP Server）
- MCPサーバの恒常ホスティング

---

### ※参考情報
1. [MCP のコンセプト (1) - コアアーキテクチャ](https://note.com/npaka/n/nfcff7807009b)
2. [自作 MCP Server Hands-On Part1: 補足編](https://qiita.com/daikumatan/items/1bd7cd532e2de5c7f4cd#21-hello-world-python%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AE%E4%BD%9C%E6%88%90)
3. [VS Code の設定から MCPサーバーを追加して GitHub Copilot agent mode で利用してみる（安定版でも利用可能に）](https://qiita.com/youtoy/items/adfeedeedf1309f194ce)
4. [VSCodeの安定版でGitHub Copilot Agentが使えるようになったのでFigmaのコンポーネントを実装させてみた](https://zenn.dev/maronn/articles/github-coipilot-agent-and-figma-mcp)
5. [【Python】uvで始めるPythonプロジェクト](https://qiita.com/kissy24/items/0c091bb5f12d697131ae)
6. [VS Codeで .cursor/mcs.json が再利用可能だった](https://zenn.dev/kuronekopunk/articles/2025-04-vscode-mcp#.vscode%2Fmcp.json)
7. [VS CodeのGitHub Copilotで時刻を取得するMcp Server Timeを呼び出す(Model Context Protocol)](https://azure-ai-agent.hatenablog.com/entry/2025/04/03/Copilot-MCP-Server-Time)