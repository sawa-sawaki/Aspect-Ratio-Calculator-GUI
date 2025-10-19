# 📐 アスペクト比計算機 GUI (Aspect Ratio Calculator GUI)

これは、画像の**アスペクト比**（**縦横比**）を計算し、指定した比率や長さに基づいて目標とする寸法を求めるための、シンプルなデスクトップアプリケーション（GUI ツール）です。

## ✨ 機能

- **画像寸法自動取得**: 画像ファイルをドラッグ＆ドロップまたは参照して選択するだけで、元の寸法を自動で入力できます。
- **アスペクト比計算**: 元の寸法や目標とする比率に基づき、最もシンプルな整数比（例：16:9, 4:3）を計算し表示します。
- **寸法計算**: 基準となる幅または高さを入力することで、指定されたアスペクト比を維持したままの目標寸法を計算します。
- **多言語対応（I18n）**: アプリケーション内のテキストを言語ファイル（JSON）に基づいて切り替えられます。
- **設定保存**: ウィンドウのサイズ、入力値、選択された言語などの設定を自動で保存・復元します。

**注意**: 設定ファイル`user/settings.json`は、アプリケーションの初回起動時または実行中に自動で作成されます。

## 🚀 使い方

### 実行ファイル (EXE) とソースコードの配布について

本プロジェクトの使い方は 2 パターンあります。Windowsユーザーの方は、実行ファイル (EXE)を[Release ページ](https://github.com/sawa-sawaki/Aspect-Ratio-Calculator-GUI/releases)からダウンロードして使うことをおすすめします。

### 1. 実行ファイル (EXE)で使う

Windows 限定です。

#### 使い方

1.  [Release ページ](https://github.com/sawa-sawaki/Aspect-Ratio-Calculator-GUI/releases)から最新の`EXEファイルを含むZIPファイル`をダウンロードします。
2.  ダウンロードしたファイルを解凍して、フォルダ内の`EXEファイル`をダブルクリックして実行します。

### 2. ソースコードで使う

Python 環境をお持ちの方は、アプリケーションの**ソースコードファイル**から起動することもできます。

#### 必要な環境 (Prerequisites)

- Python 3.10+ (Python 3.12.9 で動作確認)
- pip (基本 Python と一緒にインストールされます)

#### 使い方

1.  ターミナル（コマンドプロンプトなど）を開き、リポジトリをクローンします。
    ```bash
    git clone https://github.com/sawa-sawaki/Aspect-Ratio-Calculator-GUI
    cd "Aspect-Ratio-Calculator-GUI"
    ```
    または、
    GitHub の Code ボタン →Download ZIP からダウンロードするか、[Release ページ](https://github.com/sawa-sawaki/Aspect-Ratio-Calculator-GUI/releases)から（`Source code (zip)`）をダウンロードし、任意の場所に解凍します。

2.  **仮想環境**（**.venv**）を作成する場合は以下を実行します。
    ```bash
    python -m venv .venv
    # Windowsの場合
    .venv\Scripts\activate
    # macOS/Linuxの場合
    source .venv/bin/activate
    ```

3.  必要なライブラリをインストールします。
    ```bash
    pip install -r requirements.txt
    ```

4.  実行方法
    コンソールで以下のコマンドを実行します。

    ```bash
    python run_gui.py
    ```

### 計算手順

1.  **【画像サイズ取得】**:
    - 「画像ファイルパス:」欄に画像を**ドラッグ＆ドロップ**するか、「**参照**」ボタンからファイルを選択します。画像サイズが自動入力されます。
    - 手動でも入力することができます。「**画像寸法計算**」ボタンを押すと、画像サイズが「横の長さ (元)」「縦の長さ (元)」に自動入力されます。
2.  **【元の画像比率計算】**:
    - 上記で入力されたサイズ、または手動で入力したサイズが「元の画像比率」の計算に使用されます。
3.  **【目標画像比率および長さ】**:
    - 目標の「横の長さ」または「縦の長さ」の**どちらか一つ**を入力します。
    - 「目標画像比率 (横:縦)」は空でも問題ありません。「目標画像比率 (横:縦)」で計算したい場合に入力します。（例: `16` と `9`）
4.  「**計算を実行**」ボタンを押すと、【計算結果】セクションに「元の画像比率 (横:縦)」「目標画像比率 (横:縦)」「横の長さ (結果)」「縦の長さ (結果)」が表示されます。

## 🔧 ファイルの配置

```
.
├── language/  <-- このフォルダ内に翻訳ファイル
│   └── ja.json
├── src/
│   ├── aspect_calculator_gui.py
│   ├── aspect_logic.py
│   ├── gui_logic.py
│   ├── localization_manager.py
│   └── settings_manager.py
├── .gitignore
├── requirements.txt
├── README.md
└── run_gui.py  <-- このファイルで起動
```

## 🌍 多言語対応 (Localization)

### 1\. 既に対応している言語（2025 年で使用者が多い順）

使用しない言語の**JSON ファイル**は、削除しても問題なく機能します。英語（en.json）は使わない場合も、とっておいた方がいいと思います。

**English**、**中文** (Zhōngwén)、**हिन्दी** (Hindī)、**Español**、**العربية** (Al-ʻArabīyah)、**বাংলা** (Bānglā)、**Français**、**Русский** (Russkiy)、**Português**、**اردو** (Urdū)、**Bahasa Indonesia**、**Deutsch**、**日本語**、**मराठी** (Marāṭhī)、**తెలుగు** (Telugu)、**Türkçe**、**தமிழ்** (Tamiḻ)、**粵語** (Yuhtyú)**/**廣東話 (Gwóngdūng wá)、**上海話** (Zånhe-wú)**/**滬語 (Hùyǔ)、**한국어** (Hangugeo)

### 2\. 新しい言語の追加

本アプリケーションは、`language`フォルダ内に**JSON ファイル**を追加することで、新しい言語に簡単に追加対応できます。

1. `language`フォルダ内に、追加したい言語コード（例: 英語なら`en.json`）のファイルを作成します。
2. 既存の言語ファイル（`ja.json`など）を参考に、全てのキーに対する翻訳テキストを記述します。
3. アプリケーションを再起動すると、設定画面の言語選択プルダウンに新しい言語名が表示され、選択できるようになります。

## 👤 作者 (Author)

- **名前**: Sawa Sawaki (沢木さわ)
- **GitHub**: [@sawa-sawaki](https://github.com/sawa-sawaki)
- **note**: [https://note.com/sawa_sawaki](https://note.com/sawa_sawaki)
