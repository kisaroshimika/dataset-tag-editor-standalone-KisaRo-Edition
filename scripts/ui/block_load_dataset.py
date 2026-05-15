from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import gradio as gr

import settings
from .ui_common import *
from .uibase import UIBase
from i18n import i18n

if TYPE_CHECKING:
    from .ui_classes import *


class LoadDatasetUI(UIBase):

    def create_ui(self, cfg_general):
        with gr.Column(variant="panel"):
            with gr.Row():
                with gr.Column(scale=3):
                    self.tb_img_directory = gr.Textbox(
                        label=i18n("dataset_dir"),
                        placeholder="C:\\directory\\of\\datasets",
                        value=cfg_general.dataset_dir,
                    )
                with gr.Column(scale=1, min_width=60):
                    self.tb_caption_file_ext = gr.Textbox(
                        label=i18n("caption_ext"),
                        placeholder=".txt (on Load and Save)",
                        value=cfg_general.caption_ext,
                    )
                with gr.Column(scale=1, min_width=80):
                    self.btn_load_datasets = gr.Button(value=i18n("load"))
                    self.btn_unload_datasets = gr.Button(value=i18n("unload"))
            with gr.Accordion(label=i18n("load_settings")):
                with gr.Row():
                    with gr.Column():
                        self.cb_load_recursive = gr.Checkbox(
                            value=cfg_general.load_recursive,
                            label=i18n("load_subdirs"),
                        )
                        self.cb_load_caption_from_filename = gr.Checkbox(
                            value=cfg_general.load_caption_from_filename,
                            label=i18n("load_filename_as_caption"),
                        )
                        self.cb_replace_new_line_with_comma = gr.Checkbox(
                            value=cfg_general.replace_new_line,
                            label=i18n("replace_newline"),
                        )
                    with gr.Column():
                        self.rb_use_interrogator = gr.Radio(
                            choices=[
                                (i18n("choice_no"), "No"),
                                (i18n("choice_if_empty"), "If Empty"),
                                (i18n("choice_overwrite"), "Overwrite"),
                                (i18n("choice_prepend"), "Prepend"),
                                (i18n("choice_append"), "Append"),
                            ],
                            value=cfg_general.use_interrogator,
                            label=i18n("use_interrogator"),
                        )
                        self.dd_intterogator_names = gr.Dropdown(
                            label=i18n("interrogators"),
                            choices=dte_instance.INTERROGATOR_NAMES,
                            value=cfg_general.use_interrogator_names,
                            interactive=True,
                            multiselect=True,
                        )
            with gr.Accordion(label=i18n("interrogator_settings"), open=False):
                with gr.Row():
                    self.sl_custom_threshold_booru = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=cfg_general.custom_threshold_booru,
                        step=0.01,
                        interactive=True,
                        label=i18n("booru_threshold"),
                    )
                with gr.Row():
                    self.sl_custom_threshold_z3d = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=cfg_general.custom_threshold_z3d,
                        step=0.01,
                        interactive=True,
                        label=i18n("z3d_threshold"),
                    )
                with gr.Row():
                    self.cb_use_custom_threshold_waifu = gr.Checkbox(
                        value=cfg_general.use_custom_threshold_waifu,
                        label=i18n("use_wd_threshold"),
                        interactive=True,
                    )
                    self.sl_custom_threshold_waifu = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=cfg_general.custom_threshold_waifu,
                        step=0.01,
                        interactive=True,
                        label=i18n("wd_threshold"),
                    )

    def set_callbacks(
        self,
        o_update_filter_and_gallery: list[gr.components.Component],
        toprow: ToprowUI,
        dataset_gallery: DatasetGalleryUI,
        filter_by_tags: FilterByTagsUI,
        filter_by_selection: FilterBySelectionUI,
        batch_edit_captions: BatchEditCaptionsUI,
        update_filter_and_gallery: Callable[[], list],
    ):
        def load_files_from_dir(
            dir: str,
            caption_file_ext: str,
            recursive: bool,
            load_caption_from_filename: bool,
            replace_new_line: bool,
            use_interrogator: str,
            use_interrogator_names: list[str],
            custom_threshold_booru: float,
            use_custom_threshold_waifu: bool,
            custom_threshold_waifu: float,
            custom_threshold_z3d: float,
            use_kohya_metadata: bool,
            kohya_json_path: str,
        ):
            interrogate_method = dte_instance.InterrogateMethod.NONE
            if use_interrogator == "If Empty":
                interrogate_method = dte_instance.InterrogateMethod.PREFILL
            elif use_interrogator == "Overwrite":
                interrogate_method = dte_instance.InterrogateMethod.OVERWRITE
            elif use_interrogator == "Prepend":
                interrogate_method = dte_instance.InterrogateMethod.PREPEND
            elif use_interrogator == "Append":
                interrogate_method = dte_instance.InterrogateMethod.APPEND

            threshold_booru = custom_threshold_booru
            threshold_waifu = custom_threshold_waifu if use_custom_threshold_waifu else -1
            threshold_z3d = custom_threshold_z3d

            dte_instance.load_dataset(
                dir,
                caption_file_ext,
                recursive,
                load_caption_from_filename,
                replace_new_line,
                interrogate_method,
                use_interrogator_names,
                threshold_booru,
                threshold_waifu,
                threshold_z3d,
                settings.current.use_temp_files,
                kohya_json_path if use_kohya_metadata else None,
                settings.current.max_resolution
            )
            imgs = dte_instance.get_filtered_imgs(filters=[])
            return (
                [imgs, []]
                + update_filter_and_gallery()
            )

        self.btn_load_datasets.click(
            fn=load_files_from_dir,
            inputs=[
                self.tb_img_directory,
                self.tb_caption_file_ext,
                self.cb_load_recursive,
                self.cb_load_caption_from_filename,
                self.cb_replace_new_line_with_comma,
                self.rb_use_interrogator,
                self.dd_intterogator_names,
                self.sl_custom_threshold_booru,
                self.cb_use_custom_threshold_waifu,
                self.sl_custom_threshold_waifu,
                self.sl_custom_threshold_z3d,
                toprow.cb_save_kohya_metadata,
                toprow.tb_metadata_output,
            ],
            outputs=[
                dataset_gallery.gl_dataset_images,
                filter_by_selection.gl_filter_images,
            ]
            + o_update_filter_and_gallery,
        )

        def unload_files():
            dte_instance.clear()
            return (
                [[], []]
                + filter_by_tags.clear_filters()
                + [batch_edit_captions.tag_select_ui_remove.cbg_tags_update()]
            )

        self.btn_unload_datasets.click(
            fn=unload_files,
            outputs=[
                dataset_gallery.gl_dataset_images,
                filter_by_selection.gl_filter_images,
            ]
            + filter_by_tags.clear_filters_output()
            + [batch_edit_captions.tag_select_ui_remove.cbg_tags]
        ).then(
            fn=lambda:update_filter_and_gallery(),
            outputs=o_update_filter_and_gallery
        )
