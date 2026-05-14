import settings

class I18n:
    TRANSLATIONS = {
        "en": {
            "tab_main": "Main",
            "tab_bulk": "Bulk Process",
            "tab_settings": "Settings",
            "ui_language": "UI Language",
            "reload_ui": "Reload UI",
            "save_settings": "Save Settings",
            "restore_defaults": "Restore Default Settings",
            
            # Single Image Tab
            "model": "Model",
            "threshold": "Threshold",
            "sort_confidence": "Sort by confidence",
            "extract_tags": "Extract Tags",
            "copy": "Copy",
            "clear": "Clear",
            "status": "Status",
            "waiting": "Waiting...",
            "extracting": "Extracting...",
            "done": "Done",
            "preview": "Preview",
            "tags_output": "Tags Output",
            "no_image": "No image selected",
            "no_model": "No model selected",
            "copied": "Copied to clipboard",
            "nothing_to_copy": "Nothing to copy",

            # Settings Descriptions
            "allowed_paths": "Path whitelist (comma separated)",
            "use_temp_files": "Use temporary files for gallery",
            "temp_directory": "Temporary directory path",
            "cleanup_tmpdir": "Cleanup temp dir on startup",
            "image_columns": "Gallery columns",
            "max_resolution": "Max thumbnail resolution (0: disable)",
            "filename_word_regex": "Regex for caption from filename",
            "filename_join_string": "Join string for filename words",
            "tagger_use_spaces": "Replace '_' with space in tags",
            "interrogator_use_cpu": "Use CPU for interrogation",
            "interrogator_keep_in_memory": "Keep models in VRAM",
            "interrogator_max_length": "Max text length (GIT only)",
            "interrogator_model_dir": "Model download directory",
            "tagger_use_rating": "Include rating tags",
            "num_cpu_worker": "CPU workers (-1: auto)",
            "batch_size_vit": "Batch size (ViT)",
            "batch_size_vit_large": "Batch size (ViT large)",
            "batch_size_convnext": "Batch size (ConvNeXt)",
            "batch_size_swinv2": "Batch size (SwinV2)",
            "batch_size_eva02_large": "Batch size (EVA-02 large)",
        },
        "jp": {
            "tab_main": "メイン",
            "tab_bulk": "一括処理",
            "tab_settings": "設定",
            "ui_language": "表示言語 (Language)",
            "reload_ui": "UIを再読み込み",
            "save_settings": "設定を保存",
            "restore_defaults": "設定を初期化",

            # Single Image Tab
            "model": "モデル",
            "threshold": "Threshold (しきい値)",
            "sort_confidence": "確率（Confidence）が高い順にソート",
            "extract_tags": "タグ抽出",
            "copy": "コピー",
            "clear": "クリア",
            "status": "ステータス",
            "waiting": "待機中",
            "extracting": "抽出中...",
            "done": "完了",
            "preview": "プレビュー",
            "tags_output": "タグ出力",
            "no_image": "画像が選択されていません",
            "no_model": "モデルが選択されていません",
            "copied": "クリップボードにコピーしました",
            "nothing_to_copy": "コピー対象がありません",

            # Settings Descriptions
            "allowed_paths": "表示許可パス (カンマ区切り)",
            "use_temp_files": "ギャラリー表示に一時ファイルを使用",
            "temp_directory": "一時ファイル保存ディレクトリ",
            "cleanup_tmpdir": "起動時に一時ファイルを削除",
            "image_columns": "ギャラリーの列数",
            "max_resolution": "サムネイルの最大解像度 (0で無効)",
            "filename_word_regex": "ファイル名からタグを読み取る正規表現",
            "filename_join_string": "ファイル名タグの結合文字",
            "tagger_use_spaces": "タグ内の '_' をスペースに置換",
            "interrogator_use_cpu": "CPUで解析を実行",
            "interrogator_keep_in_memory": "解析モデルをVRAMに保持",
            "interrogator_max_length": "最大テキスト長 (GITのみ)",
            "interrogator_model_dir": "モデル保存ディレクトリ",
            "tagger_use_rating": "レーティングタグを含める",
            "num_cpu_worker": "CPUワーカー数 (-1で自動)",
            "batch_size_vit": "バッチサイズ (ViT)",
            "batch_size_vit_large": "バッチサイズ (ViT large)",
            "batch_size_convnext": "バッチサイズ (ConvNeXt)",
            "batch_size_swinv2": "バッチサイズ (SwinV2)",
            "batch_size_eva02_large": "バッチサイズ (EVA-02 large)",
        }
    }

    def __call__(self, key):
        lang = getattr(settings.current, "ui_language", "en")
        if lang not in self.TRANSLATIONS:
            lang = "en"
        return self.TRANSLATIONS[lang].get(key, key)

# シングルトンとしてエクスポート
i18n = I18n()
