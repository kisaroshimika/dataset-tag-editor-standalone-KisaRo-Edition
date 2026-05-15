# Dataset Tag Editor Standalone - KisaRo Edition

[English Readme](README.md)

本プロジェクトは、toshiaki1729氏による [Dataset Tag Editor Standalone](https://github.com/toshiaki1729/dataset-tag-editor-standalone) をベースに機能追加・改良を行った派生版（KisaRo Edition）です。

WebUI 上で学習用データセットのキャプションを直感的に編集でき、特にカンマ区切り形式のタグ編集に最適化されています。

## KisaRo Edition での追加機能
- **多言語表示対応 (日本語/英語)**: UI表示を日本語と英語で切り替えられるようになりました。「Settings」タブから設定可能です。
- **メインタブ (単一画像用Tagger) の追加**: 画像をドラッグ＆ドロップするだけで、素早くタグを解析・確認できる専用の「Main」タブを実装しました。
- **UI/UXの改善**: より快適にタグ編集が行えるよう、細かな調整やデフォルト設定のカスタマイズ機能を追加しています。

## オリジナルプロジェクトについて
本ツールは [toshiaki1729](https://github.com/toshiaki1729) 氏の著作物をベースにしています。派生版としての公開にあたり、オリジナルの素晴らしい成果に深く感謝いたします。

オリジナルリポジトリ: [https://github.com/toshiaki1729/dataset-tag-editor-standalone](https://github.com/toshiaki1729/dataset-tag-editor-standalone)

---

## 動作要件
要件は `requirements.txt` に全て記載されています。
**はじめに以下をインストールしてください：**
- [Python](https://www.python.org/) >= 3.9 (3.10.11で開発)
- [PyTorch](https://pytorch.org/) with CUDA >= 1.10.0

## インストール方法
### Windows
`install.bat` を実行してください。

### Linux (または手動インストール)
リポジトリのルートディレクトリで以下のコマンドを実行します：
```sh
python3 -m venv --system-site-packages venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## 起動方法
### Windows
`launch_user.bat` を実行してください。

### Linux
```sh
source ./venv/bin/activate
python scripts/launch.py [arguments]
```

## 主な機能
- テキスト形式およびJSON形式のキャプション編集
- 画像を見ながらの個別・一括編集
- 複数タグによる強力な絞り込み (AND/OR/NOT)
- 正規表現対応の一括置換・削除・追加
- 各種 Interrogator (BLIP, DeepDanbooru, WDv1.4 Tagger v1/v2/v3 等) のサポート
- UI上からのファイル移動・削除
