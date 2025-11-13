# QuadrantChart
案件推進判断のための四象限分析ツール

## 環境構築

### 必要な環境
- Python 3.14以上
- uv（Pythonパッケージマネージャー）

### uv のインストール

Windows:
```bash
pip install uv
```

### プロジェクト環境の構築

リポジトリをクローンしてプロジェクトディレクトリに移動：
```bash
git clone https://github.com/agukwt/QuadrantChart.git
cd QuadrantChart
```

初回セットアップ:
```bash
uv sync
```

このコマンドにより[`pyproject.toml`](pyproject.toml) と [`uv.lock`](uv.lock) から同じ環境が復現されます。
- [`pyproject.toml`](pyproject.toml) に記載されたすべての依存パッケージがインストールされます
- `.venv` 仮想環境が作成されます
- [`uv.lock`](uv.lock) が生成/更新されます

## 実行方法

スクリプトを実行:
```bash
uv run main.py
```

実行後、プロジェクトルートに **`quadrant_analysis_result.png`** が生成されます。
このファイルが四象限分析の可視化結果です。

### 出力ファイルの確認
- ファイル名：`quadrant_analysis_result.png`
- 場所：プロジェクトルート（`QuadrantChart/` ディレクトリ直下）
- 内容：案件のプロット、象限ラベル、閾値ラインが表示されます

または手動で仮想環境を有効化（非推奨）:
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows cmd
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# その後
python main.py
```

## 依存パッケージ管理

### 新しいライブラリを追加する場合

```bash
uv add <package-name>
```
`uv add` コマンドにより：
- `pyproject.toml` にパッケージが追加される
- `uv.lock` に具体的なバージョンが自動的に書き込まれる
- `.venv` にインストールされる

例：
```bash
uv add pandas
```

### パッケージ一覧を確認

```bash
uv pip list
```

### 環境の更新

```bash
uv lock --upgrade      # uv.lock に最新バージョンを確定
uv sync                # .venv に反映
```

## ファイル構成

```
QuadrantChart/
├── main.py              # メインスクリプト
├── pyproject.toml       # 依存パッケージ定義
├── uv.lock              # ロックファイル（環境の完全復現用）
├── config.ini           # 設定ファイル（オプション）
└── README.md
```

## チームでの使用

1. リポジトリをクローン
2. プロジェクトディレクトリに移動
3. 以下を実行：
   ```bash
   uv sync
   uv run main.py
   ```

[`pyproject.toml`](pyproject.toml) と [`uv.lock`](uv.lock) で完全に同じ環境が復現されます。

## トラブルシューティング

### キャッシュをクリアしたい場合
```bash
uv cache clean
uv sync
```

### 仮想環境を再作成したい場合
```bash
Remove-Item -Recurse -Force .venv
uv sync
```

## 設定ファイル

`config.ini` にて閾値をカスタマイズ可能です：

```ini
[THRESHOLD_DEFAULTS]
rev_threshold = 1.0
prof_threshold = 0.5
```