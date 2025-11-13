import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from dataclasses import dataclass
import configparser
import os


# --- 1. グローバル閾値と設定ファイルの定義 ---
CONFIG_FILE_PATH = 'config.ini'

# コード内のデフォルト値 (config.iniが存在しない場合のフォールバック)
GLOBAL_REV_THRESHOLD = 1.0
GLOBAL_PROF_THRESHOLD = 0.5


# --- 2. 案件データ Dataclass の定義 ---
@dataclass
class ProjectData:
    """案件名と2つの効率値を格納するためのデータクラス"""
    name: str
    revenue_efficiency: float
    profit_efficiency: float


# --- 3. フォント設定 ---
JP_FONT = fm.FontProperties(family='Meiryo', size=14)
JP_FONT_SMALL = fm.FontProperties(family='Meiryo', size=10)
plt.rcParams['axes.unicode_minus'] = False


# --- 4. 閾値管理関数 ---
def load_default_thresholds(config_file_path=CONFIG_FILE_PATH):
    """
    config.ini からデフォルト閾値を読み込み、グローバル変数を初期化する。
    """
    global GLOBAL_REV_THRESHOLD, GLOBAL_PROF_THRESHOLD

    config = configparser.ConfigParser()

    if not os.path.exists(config_file_path):
        print(f"WARN: 設定ファイル '{config_file_path}' が見つかりません。コード内のデフォルト値を使用します。")
        return

    try:
        config.read(config_file_path)

        if 'THRESHOLD_DEFAULTS' in config:
            rev_th_from_config = config.getfloat('THRESHOLD_DEFAULTS', 'rev_threshold', fallback=GLOBAL_REV_THRESHOLD)
            prof_th_from_config = config.getfloat('THRESHOLD_DEFAULTS',
                                                  'prof_threshold', fallback=GLOBAL_PROF_THRESHOLD)

            GLOBAL_REV_THRESHOLD = rev_th_from_config
            GLOBAL_PROF_THRESHOLD = prof_th_from_config

            print(f"INFO: デフォルト閾値が {config_file_path} からロードされました: "
                  f"Rev TH={GLOBAL_REV_THRESHOLD:.2f}, Prof TH={GLOBAL_PROF_THRESHOLD:.2f}")

    except configparser.Error as e:
        print(f"ERROR: config.ini の解析に失敗しました。エラー: {e}")
    except Exception as e:
        print(f"ERROR: 閾値のロード中に予期せぬエラーが発生しました: {e}")


def load_or_update_thresholds(rev_th_override=None, prof_th_override=None):
    """
    Agent がチャットからの指示に基づいて閾値を更新するための関数。
    """
    global GLOBAL_REV_THRESHOLD, GLOBAL_PROF_THRESHOLD

    if rev_th_override is not None:
        try:
            float_val = float(rev_th_override)
            GLOBAL_REV_THRESHOLD = float_val
            print(f"UPDATE: ユーザーの指示により Rev TH が {float_val:.2f} に上書きされました。")
        except ValueError:
            print(f"ERROR: 無効な Rev TH 値 '{rev_th_override}' が指定されました。変更をスキップします。")

    if prof_th_override is not None:
        try:
            float_val = float(prof_th_override)
            GLOBAL_PROF_THRESHOLD = float_val
            print(f"UPDATE: ユーザーの指示により Prof TH が {float_val:.2f} に上書きされました。")
        except ValueError:
            print(f"ERROR: 無効な Prof TH 値 '{prof_th_override}' が指定されました。変更をスキップします。")


# --- 5. 可視化機能 (main.py のプロット形式を採用) ---
def visualize_quadromatrix(
        projects_data: list[ProjectData], highlight_project_name: str = None) -> dict:
    """
    案件データを四象限マトリクスで可視化する。
    閾値はグローバル変数 GLOBAL_REV_THRESHOLD, GLOBAL_PROF_THRESHOLD を参照する。
    """

    # グローバル変数から閾値を取得
    rev_threshold = GLOBAL_REV_THRESHOLD
    prof_threshold = GLOBAL_PROF_THRESHOLD

    if not projects_data:
        print("ERROR: プロジェクトデータが空です。")
        return {"image_path": None}

    project_names = [p.name for p in projects_data]
    rev_eff = [p.revenue_efficiency for p in projects_data]
    prof_eff = [p.profit_efficiency for p in projects_data]

    # プロット作成
    plt.figure(figsize=(10, 8))

    # 通常のポイントをプロット
    plt.scatter(rev_eff, prof_eff, color='black', s=50, alpha=0.7)

    # 標準線 (閾値) の描画
    plt.axhline(y=prof_threshold, color='black', linestyle='--', linewidth=1.5, label='Standard Profit Efficiency')
    plt.axvline(x=rev_threshold, color='black', linestyle='--', linewidth=1.5, label='Standard Revenue Efficiency')

    # --- 軸の範囲を計算 (閾値が4象限で等分に分かれるように設定) ---
    max_rev = rev_threshold * 2
    max_prof = prof_threshold * 2

    # プロット値が閾値を超える場合、プロット値の1.2倍を最大値とする
    max_rev = max(rev_eff) * 1.2 if max(rev_eff) > max_rev else max_rev
    max_prof = max(prof_eff) * 1.2 if max(prof_eff) > max_prof else max_prof

    # 閾値が各象限で等分に分かれるように設定
    # 閾値を中心に、負側と正側で等距離を確保
    min_rev = 0
    min_prof = 0

    # X軸: 閾値の左側を [0, rev_threshold]、右側を [rev_threshold, max_rev] に設定
    # Y軸: 閾値の下側を [0, prof_threshold]、上側を [prof_threshold, max_prof] に設定
    plt.xlim(min_rev, max_rev)
    plt.ylim(min_prof, max_prof)

    # 最終的なプロット範囲を取得
    x_limit = plt.xlim()
    y_limit = plt.ylim()
    x_max = x_limit[1]

    # 中央Y座標を標準値よりわずかに上/下に設定
    y_center_upper = y_limit[1] * 0.95
    y_center_lower = prof_threshold - (prof_threshold - min_prof) * 0.05

    # --- 象限のラベリング ---
    # I 象限
    x_i = rev_threshold + (x_max - rev_threshold) / 2
    plt.text(x_i, y_center_upper,
             'I: 最優先推進',
             fontsize=12, color='darkgreen', ha='center', va='bottom', weight='bold', fontproperties=JP_FONT_SMALL)

    # II 象限
    x_ii = min_rev + (rev_threshold - min_rev) / 2
    plt.text(x_ii, y_center_upper,
             'II: 収益改善が必要',
             fontsize=12, color='darkorange', ha='center', va='bottom', fontproperties=JP_FONT_SMALL)

    # III 象限
    x_iii = min_rev + (rev_threshold - min_rev) / 2
    plt.text(x_iii, y_center_lower,
             'III: 検討するだけ無駄',
             fontsize=12, color='#1a1a1a', ha='center', va='top', fontproperties=JP_FONT_SMALL)

    # IV 象限
    x_iv = rev_threshold + (x_max - rev_threshold) / 2
    plt.text(x_iv, y_center_lower,
             'IV: 利益改善が必要',
             fontsize=12, color='darkorange', ha='center', va='top', fontproperties=JP_FONT_SMALL)

    # --- プロットの装飾 ---
    plt.title('案件推進判断のための財務メトリクス (四象限分析)', fontsize=20, fontproperties=JP_FONT)
    plt.xlabel('売上効率', fontsize=14, fontproperties=JP_FONT)
    plt.ylabel('利益効率', fontsize=14, fontproperties=JP_FONT)
    plt.grid(True, linestyle=':', alpha=0.6)

    # 目盛りを内側に設定
    plt.tick_params(axis='both', which='major', direction='in')

    # 各案件に名前を付ける
    for i, name in enumerate(project_names):
        # ハイライト対象の場合は色を変える
        color = 'red' if name == highlight_project_name else 'black'
        weight = 'bold' if name == highlight_project_name else 'normal'

        plt.annotate("{name} [{rev_eff:.2f}, {prof_eff:.2f}]".format(
            name=name, rev_eff=rev_eff[i], prof_eff=prof_eff[i]),
            (rev_eff[i], prof_eff[i]), xytext=(5, 5),
            textcoords='offset points', fontproperties=JP_FONT_SMALL,
            color=color, weight=weight)

    output_image_path = "quadrant_analysis_result.png"
    plt.savefig(output_image_path, dpi=100, bbox_inches='tight')
    # plt.show()

    return {
        "image_path": output_image_path
    }


# --- 起動時処理 ---
if __name__ == "__main__":
    print("Hello from quadrantchart main!")

    load_default_thresholds()

    visualize_quadromatrix(
        projects_data=[
            ProjectData("A", 1.5, 0.7),
            ProjectData("B", 0.8, 0.6),
            ProjectData("C", 1.2, 0.3),
            ProjectData("D", 0.6, 0.2),
            ProjectData("E", 2.2, 0.9),
            ProjectData("F", 0.9, 0.4)
        ],
        highlight_project_name="F"
    )
