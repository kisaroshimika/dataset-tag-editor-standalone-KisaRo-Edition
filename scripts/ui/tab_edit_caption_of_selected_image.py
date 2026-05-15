from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import gradio as gr

from dte_instance import dte_module
from utilities import wrap_queued_call

from .ui_common import *
from .uibase import UIBase
from tokenizer import clip_tokenizer
from i18n import i18n

if TYPE_CHECKING:
    from .ui_classes import *

SortBy = dte_instance.SortBy
SortOrder = dte_instance.SortOrder


class EditCaptionOfSelectedImageUI(UIBase):
    def __init__(self):
        self.change_is_saved = True
        self.prev_idx = -1
        self.current_idx = -1

    def create_ui(self, cfg_edit_selected):
        with gr.Row(visible=False):
            self.nb_hidden_image_index_save_or_not = gr.Number(
                value=-1, label="hidden_s_or_n"
            )
            self.tb_hidden_edit_caption = gr.Textbox()
            self.btn_hidden_save_caption = gr.Button(
                elem_id="btn_hidden_save_caption"
            )
        with gr.Tab(label=i18n("read_caption_selected")):
            self.tb_caption = gr.Textbox(
                label=i18n("caption_selected"),
                interactive=False,
                lines=6,
                elem_id="dte_caption",
            )
            self.token_counter_caption = gr.HTML(
                value="<span>0/75</span>", elem_id="dte_caption_counter", elem_classes=["token-counter"]
            )
            with gr.Row():
                self.btn_copy_caption = gr.Button(value=i18n("copy_and_overwrite"))
                self.btn_prepend_caption = gr.Button(value=i18n("prepend"))
                self.btn_append_caption = gr.Button(value=i18n("append"))

        with gr.Tab(label=i18n("interrogate_selected")):
            with gr.Row():
                self.dd_intterogator_names_si = gr.Dropdown(
                    label=i18n("interrogator"),
                    choices=dte_instance.INTERROGATOR_NAMES,
                    value=cfg_edit_selected.use_interrogator_name,
                    interactive=True,
                    multiselect=False,
                )
                self.btn_interrogate_si = gr.Button(value=i18n("interrogate"))
            with gr.Column():
                self.tb_interrogate = gr.Textbox(
                    label=i18n("interrogate_result"),
                    interactive=True,
                    lines=6,
                    elem_id="dte_interrogate",
                )
                self.token_counter_interrogate = gr.HTML(
                    value="<span>0/75</span>", elem_id="dte_interrogate_counter", elem_classes=["token-counter"]
                )
            with gr.Row():
                self.btn_copy_interrogate = gr.Button(value=i18n("copy_and_overwrite"))
                self.btn_prepend_interrogate = gr.Button(value=i18n("prepend"))
                self.btn_append_interrogate = gr.Button(value=i18n("append"))
        with gr.Column():
            self.cb_copy_caption_automatically = gr.Checkbox(
                value=cfg_edit_selected.auto_copy,
                label=i18n("auto_copy_caption"),
            )
            self.cb_sort_caption_on_save = gr.Checkbox(
                value=cfg_edit_selected.sort_on_save, label=i18n("sort_on_save")
            )
            with gr.Row(visible=cfg_edit_selected.sort_on_save) as self.sort_settings:
                self.rb_sort_by = gr.Radio(
                    choices=[
                        (i18n("choice_alpha"), SortBy.ALPHA),
                        (i18n("choice_frequency"), SortBy.FREQ),
                        (i18n("choice_length"), SortBy.LEN),
                    ],
                    value=cfg_edit_selected.sort_by,
                    interactive=True,
                    label=i18n("sort_by"),
                )
                self.rb_sort_order = gr.Radio(
                    choices=[
                        (i18n("choice_asc"), SortOrder.ASC),
                        (i18n("choice_desc"), SortOrder.DESC),
                    ],
                    value=cfg_edit_selected.sort_order,
                    interactive=True,
                    label=i18n("sort_order"),
                )
            self.cb_ask_save_when_caption_changed = gr.Checkbox(
                value=cfg_edit_selected.warn_change_not_saved,
                label=i18n("warn_unsaved"),
            )
        with gr.Column():
            self.tb_edit_caption = gr.Textbox(
                label=i18n("edit_tags"),
                interactive=True,
                lines=6,
                elem_id="dte_edit_caption",
            )
            self.token_counter_edit_caption = gr.HTML(
                value="<span>0/75</span>", elem_id="dte_edit_caption_counter", elem_classes=["token-counter"]
            )
        self.btn_apply_changes_selected_image = gr.Button(
            value=i18n("apply_to_selected"), variant="primary"
        )
        self.btn_apply_changes_all_images = gr.Button(
            value=i18n("apply_to_all_displayed"), variant="primary"
        )

        gr.HTML(
            i18n("note_save_all_changes")
        )

    def set_callbacks(
        self,
        o_update_filter_and_gallery: list[gr.components.Component],
        dataset_gallery: DatasetGalleryUI,
        load_dataset: LoadDatasetUI,
        get_filters: Callable[[], list[dte_module.filters.Filter]],
        update_filter_and_gallery: Callable[[], list],
    ):
        load_dataset.btn_load_datasets.click(
            fn=lambda: ["", -1],
            outputs=[self.tb_caption, self.nb_hidden_image_index_save_or_not],
        )

        def gallery_index_changed(
            select_data: gr.SelectData,
            edit_caption: str,
            copy_automatically: bool,
            warn_change_not_saved: bool,
        ):
            self.prev_idx = self.current_idx
            self.current_idx = select_data.index if select_data.selected else -1
            img_paths = dte_instance.get_filtered_imgpaths(filters=get_filters())
            prev_tags_txt = ""
            if 0 <= self.prev_idx and self.prev_idx < len(img_paths):
                prev_tags_txt = ", ".join(
                    dte_instance.get_tags_by_image_path(img_paths[self.prev_idx])
                )
            else:
                self.prev_idx = -1

            next_tags_txt = ""
            if 0 <= self.current_idx and self.current_idx < len(img_paths):
                next_tags_txt = ", ".join(
                    dte_instance.get_tags_by_image_path(img_paths[self.current_idx])
                )

            return \
                [
                    self.prev_idx
                    if warn_change_not_saved
                    and edit_caption != prev_tags_txt
                    and not self.change_is_saved
                    else -1
                ]\
                + [next_tags_txt, next_tags_txt if copy_automatically else edit_caption]\
                + [edit_caption]

        self.nb_hidden_image_index_save_or_not.change(
            fn=lambda a: None,
            js="(a) => ask_save_change_or_not(a)",
            inputs=self.nb_hidden_image_index_save_or_not,
        )
        dataset_gallery.gl_dataset_images.select(
            fn=gallery_index_changed,
            inputs=[
                self.tb_edit_caption,
                self.cb_copy_caption_automatically,
                self.cb_ask_save_when_caption_changed,
            ],
            outputs=[self.nb_hidden_image_index_save_or_not]
            + [self.tb_caption, self.tb_edit_caption]
            + [self.tb_hidden_edit_caption],
        )

        def change_selected_image_caption(
            tags_text: str, idx: int, sort: bool, sort_by: str, sort_order: str
        ):
            idx = int(idx)
            img_paths = dte_instance.get_filtered_imgpaths(filters=get_filters())

            edited_tags = [t.strip() for t in tags_text.split(",")]
            edited_tags = [t for t in edited_tags if t]

            if sort:
                edited_tags = dte_instance.sort_tags(
                    edited_tags, SortBy(sort_by), SortOrder(sort_order)
                )

            if 0 <= idx and idx < len(img_paths):
                dte_instance.set_tags_by_image_path(
                    imgpath=img_paths[idx], tags=edited_tags
                )
            return update_filter_and_gallery()

        self.btn_hidden_save_caption.click(
            fn=change_selected_image_caption,
            inputs=[
                self.tb_hidden_edit_caption,
                self.nb_hidden_image_index_save_or_not,
                self.cb_sort_caption_on_save,
                self.rb_sort_by,
                self.rb_sort_order,
            ],
            outputs=o_update_filter_and_gallery,
        )

        self.btn_copy_caption.click(
            fn=lambda a: a, inputs=[self.tb_caption], outputs=[self.tb_edit_caption]
        )

        self.btn_append_caption.click(
            fn=lambda a, b: b + (", " if a and b else "") + a,
            inputs=[self.tb_caption, self.tb_edit_caption],
            outputs=[self.tb_edit_caption],
        )

        self.btn_prepend_caption.click(
            fn=lambda a, b: a + (", " if a and b else "") + b,
            inputs=[self.tb_caption, self.tb_edit_caption],
            outputs=[self.tb_edit_caption],
        )

        def interrogate_selected_image(
            interrogator_name: str,
            threshold_booru: float,
            use_threshold_waifu: bool,
            threshold_waifu: float,
            threshold_z3d: float,
        ):
            if not interrogator_name:
                return ""
            threshold_booru = (
                threshold_booru
            )
            threshold_waifu = threshold_waifu if use_threshold_waifu else -1
            return dte_instance.interrogate_image(
                dataset_gallery.selected_path,
                interrogator_name,
                threshold_booru,
                threshold_waifu,
                threshold_z3d,
            )

        self.btn_interrogate_si.click(
            fn=interrogate_selected_image,
            inputs=[
                self.dd_intterogator_names_si,
                load_dataset.sl_custom_threshold_booru,
                load_dataset.cb_use_custom_threshold_waifu,
                load_dataset.sl_custom_threshold_waifu,
                load_dataset.sl_custom_threshold_z3d,
            ],
            outputs=[self.tb_interrogate],
        )

        self.btn_copy_interrogate.click(
            fn=lambda a: a, inputs=[self.tb_interrogate], outputs=[self.tb_edit_caption]
        )

        self.btn_append_interrogate.click(
            fn=lambda a, b: b + (", " if a and b else "") + a,
            inputs=[self.tb_interrogate, self.tb_edit_caption],
            outputs=[self.tb_edit_caption],
        )

        self.btn_prepend_interrogate.click(
            fn=lambda a, b: a + (", " if a and b else "") + b,
            inputs=[self.tb_interrogate, self.tb_edit_caption],
            outputs=[self.tb_edit_caption],
        )

        def change_in_caption():
            self.change_is_saved = False

        self.tb_edit_caption.change(fn=change_in_caption)

        self.tb_caption.change(fn=change_in_caption)

        def apply_changes(edited: str, sort: bool, sort_by: str, sort_order: str):
            self.change_is_saved = True
            return change_selected_image_caption(
                edited, dataset_gallery.selected_index, sort, sort_by, sort_order
            )

        self.btn_apply_changes_selected_image.click(
            fn=apply_changes,
            inputs=[
                self.tb_edit_caption,
                self.cb_sort_caption_on_save,
                self.rb_sort_by,
                self.rb_sort_order,
            ],
            outputs=o_update_filter_and_gallery
        )

        def apply_chages_all(tags_text: str, sort: bool, sort_by: str, sort_order: str):
            self.change_is_saved = True
            img_paths = dte_instance.get_filtered_imgpaths(filters=get_filters())

            edited_tags = [t.strip() for t in tags_text.split(",")]
            edited_tags = [t for t in edited_tags if t]

            if sort:
                edited_tags = dte_instance.sort_tags(
                    edited_tags, SortBy(sort_by), SortOrder(sort_order)
                )

            for img_path in img_paths:
                dte_instance.set_tags_by_image_path(imgpath=img_path, tags=edited_tags)
            return update_filter_and_gallery()

        self.btn_apply_changes_all_images.click(
            fn=apply_chages_all,
            inputs=[
                self.tb_edit_caption,
                self.cb_sort_caption_on_save,
                self.rb_sort_by,
                self.rb_sort_order,
            ],
            outputs=o_update_filter_and_gallery
        )

        self.cb_sort_caption_on_save.change(
            fn=lambda x: gr.update(visible=x),
            inputs=self.cb_sort_caption_on_save,
            outputs=self.sort_settings,
        )

        def update_token_counter(text: str):
            _, token_count = clip_tokenizer.tokenize(text)
            max_length = clip_tokenizer.get_target_token_count(token_count)
            return (
                f"<span class='gr-box gr-text-input'>{token_count}/{max_length}</span>"
            )

        update_caption_token_counter_args = {
            "fn": wrap_queued_call(update_token_counter),
            "inputs": [self.tb_caption],
            "outputs": [self.token_counter_caption],
        }
        update_edit_caption_token_counter_args = {
            "fn": wrap_queued_call(update_token_counter),
            "inputs": [self.tb_edit_caption],
            "outputs": [self.token_counter_edit_caption],
        }
        update_interrogate_token_counter_args = {
            "fn": wrap_queued_call(update_token_counter),
            "inputs": [self.tb_interrogate],
            "outputs": [self.token_counter_interrogate],
        }

        self.tb_caption.change(**update_caption_token_counter_args)
        self.tb_edit_caption.change(**update_edit_caption_token_counter_args)
        self.tb_interrogate.change(**update_interrogate_token_counter_args)
