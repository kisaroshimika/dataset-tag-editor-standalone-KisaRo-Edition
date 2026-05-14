from PIL import Image

import gradio as gr

from dte_instance import dte_instance
from dataset_tag_editor import taggers_builtin
import logger
from i18n import i18n


def get_tagger_model_names():
    """WD系Tagger + DeepDanbooru + Z3D のモデル名リストを返す"""
    tagger_names = []
    for it in dte_instance.INTERROGATORS:
        if isinstance(it, (
            taggers_builtin.WaifuDiffusion,
            taggers_builtin.WaifuDiffusionTimm,
            taggers_builtin.DeepDanbooru,
            taggers_builtin.Z3D_E621,
        )):
            tagger_names.append(it.name())
    return tagger_names


def extract_tags(image, model_name, threshold, sort_by_confidence):
    """画像からタグを抽出する"""
    if image is None:
        return "", i18n("no_image")

    if not model_name:
        return "", i18n("no_model")

    try:
        logger.write(f"タグ抽出開始: model={model_name}, threshold={threshold}")
        results = dte_instance.interrogate_single_image(
            image, model_name, threshold, sort_by_confidence=sort_by_confidence
        )

        if not results:
            return "", "タグが抽出できませんでした"

        tag_str = ", ".join([tag for tag, _ in results])
        status = f"{i18n('done')} — {len(results)} tags"
        logger.write(f"Tags extracted: {len(results)} tags")
        return tag_str, status

    except Exception as e:
        error_msg = f"エラー: {str(e)}"
        logger.error(error_msg)
        return "", error_msg


def on_ui_tabs():
    tagger_names = get_tagger_model_names()
    # デフォルトモデル: wd-eva02-large-tagger-v3
    default_model = "wd-eva02-large-tagger-v3"
    if default_model not in tagger_names:
        default_model = tagger_names[-1] if tagger_names else ""

    with gr.Blocks(elem_id="single_image_tab") as interface:
        # ---- 上部コントロール行 ----
        with gr.Row(elem_classes="controls-row"):
            dd_model = gr.Dropdown(
                label=i18n("model"),
                choices=tagger_names,
                value=default_model,
                scale=4,
            )
            nb_threshold = gr.Number(
                label=i18n("threshold"),
                value=0.5296,
                minimum=0.0,
                maximum=1.0,
                step=0.01,
                scale=1,
            )
            cb_sort_confidence = gr.Checkbox(
                label=i18n("sort_confidence"),
                value=False,
                scale=1,
            )
            with gr.Column(scale=2, elem_classes="action-buttons"):
                with gr.Row():
                    btn_extract = gr.Button(i18n("extract_tags"), variant="primary")
                    btn_copy = gr.Button(i18n("copy"), variant="secondary")
                with gr.Row():
                    btn_clear = gr.Button(i18n("clear"), variant="secondary")

        # ---- ステータス ----
        tb_status = gr.Textbox(
            label="",
            value=i18n("waiting"),
            interactive=False,
            elem_id="single_image_status",
        )

        # ---- メイン表示エリア（2カラム） ----
        with gr.Row(elem_classes="result-row", equal_height=True):
            with gr.Column(scale=1):
                gr.Markdown(f"### {i18n('preview')}")
                img_preview = gr.Image(
                    label=None,
                    type="pil",
                    elem_id="single_image_preview",
                    height=500,
                    interactive=True,
                )
            with gr.Column(scale=1):
                gr.Markdown(f"### {i18n('tags_output')}")
                tb_tags = gr.Textbox(
                    label=None,
                    value="",
                    lines=20,
                    max_lines=40,
                    interactive=True,
                    elem_id="single_image_tags",
                )

        # ================================================================
        # コールバック
        # ================================================================

        def on_image_change(image, model_name, threshold, sort_by_confidence):
            """画像読み込み時に自動でタグ抽出"""
            if image is None:
                return "", i18n("waiting")
            return extract_tags(image, model_name, threshold, sort_by_confidence)

        def on_extract_click(image, model_name, threshold, sort_by_confidence):
            """タグ抽出ボタン"""
            return extract_tags(image, model_name, threshold, sort_by_confidence)

        def on_clear_click():
            """クリアボタン"""
            return None, "", i18n("waiting")

        def on_copy_done(tags):
            """コピー完了のステータス更新"""
            if tags:
                return i18n("copied")
            return i18n("nothing_to_copy")

        # 画像変更時 → 自動タグ抽出
        img_preview.change(
            fn=on_image_change,
            inputs=[img_preview, dd_model, nb_threshold, cb_sort_confidence],
            outputs=[tb_tags, tb_status],
        )

        # タグ抽出ボタン
        btn_extract.click(
            fn=on_extract_click,
            inputs=[img_preview, dd_model, nb_threshold, cb_sort_confidence],
            outputs=[tb_tags, tb_status],
        )

        # クリアボタン
        btn_clear.click(
            fn=on_clear_click,
            inputs=[],
            outputs=[img_preview, tb_tags, tb_status],
        )

        # コピーボタン（JavaScript でクリップボードにコピー + ステータス更新）
        btn_copy.click(
            fn=on_copy_done,
            inputs=[tb_tags],
            outputs=[tb_status],
            js="() => { copyTagsToClipboard(); }",
        )

    return interface
