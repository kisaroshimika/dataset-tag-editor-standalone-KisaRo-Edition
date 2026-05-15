from __future__ import annotations
from typing import TYPE_CHECKING, Callable

import gradio as gr

from .ui_common import *
from .uibase import UIBase
from i18n import i18n

if TYPE_CHECKING:
    from .ui_classes import *


class MoveOrDeleteFilesUI(UIBase):
    def __init__(self):
        self.target_data = "Selected One"
        self.current_target_txt = ""
        self.update_func = None
        self.update_args = None

    def create_ui(self, cfg_file_move_delete):
        gr.HTML(value=i18n("note_unload"))
        self.target_data = cfg_file_move_delete.range
        self.rb_move_or_delete_target_data = gr.Radio(
            choices=[
                (i18n("choice_selected_one"), "Selected One"),
                (i18n("choice_all_displayed"), "All Displayed Ones"),
            ],
            value=cfg_file_move_delete.range,
            label=i18n("move_or_delete_label"),
        )
        self.cbg_move_or_delete_target_file = gr.CheckboxGroup(
            choices=[
                (i18n("choice_image_file"), "Image File"),
                (i18n("choice_caption_file"), "Caption Text File"),
                (i18n("choice_backup_file"), "Caption Backup File"),
            ],
            label=i18n("target"),
            value=cfg_file_move_delete.target,
        )
        self.tb_move_or_delete_caption_ext = gr.Textbox(
            label=i18n("caption_ext"),
            placeholder="txt",
            value=cfg_file_move_delete.caption_ext,
        )
        self.ta_move_or_delete_target_dataset_num = gr.HTML(
            value=f"{i18n('target_num')}0"
        )
        self.tb_move_or_delete_destination_dir = gr.Textbox(
            label=i18n("destination_dir"), value=cfg_file_move_delete.destination
        )
        self.btn_move_or_delete_move_files = gr.Button(
            value=i18n("move_files"), variant="primary"
        )
        gr.HTML(
            value=i18n("note_delete")
        )
        self.btn_move_or_delete_delete_files = gr.Button(
            value=i18n("delete_files"), variant="primary"
        )
    
    def update_current_move_or_delete_target_num(self):
        if self.update_func:
            text = self.update_func(self.target_data)
            return gr.HTML(text)
        else:
            return self.ta_move_or_delete_target_dataset_num

    def set_callbacks(
        self,
        o_update_filter_and_gallery: list[gr.components.Component],
        dataset_gallery: DatasetGalleryUI,
        get_filters: Callable[[], list[dte_module.filters.Filter]],
        update_filter_and_gallery: Callable[[], list],
    ):
        def _get_current_move_or_delete_target_num(text:str):
            self.target_data = text
            if self.target_data == "Selected One":
                self.current_target_txt = f"{i18n('target_num')}{1 if dataset_gallery.selected_index != -1 else 0}"
            elif self.target_data == "All Displayed Ones":
                img_paths = dte_instance.get_filtered_imgpaths(filters=get_filters())
                self.current_target_txt = f"{i18n('target_num')}{len(img_paths)}"
            else:
                self.current_target_txt = f"{i18n('target_num')}0"
            return self.current_target_txt

        
        self.update_func = _get_current_move_or_delete_target_num

        self.update_args = {
            "fn": self.update_func,
            "inputs": [self.rb_move_or_delete_target_data],
            "outputs": [self.ta_move_or_delete_target_dataset_num],
        }

        self.rb_move_or_delete_target_data.change(**self.update_args)

        def move_files(
            target_data: str, target_file: list[str], caption_ext: str, dest_dir: str
        ):
            move_img = "Image File" in target_file
            move_txt = "Caption Text File" in target_file
            move_bak = "Caption Backup File" in target_file
            if target_data == "Selected One":
                img_path = dataset_gallery.selected_path
                if img_path:
                    dte_instance.move_dataset_file(
                        img_path, caption_ext, dest_dir, move_img, move_txt, move_bak
                    )
                    dte_instance.construct_tag_infos()

            elif target_data == "All Displayed Ones":
                dte_instance.move_dataset(
                    dest_dir, caption_ext, get_filters(), move_img, move_txt, move_bak
                )

            return update_filter_and_gallery()

        self.btn_move_or_delete_move_files.click(
            fn=move_files,
            inputs=[
                self.rb_move_or_delete_target_data,
                self.cbg_move_or_delete_target_file,
                self.tb_move_or_delete_caption_ext,
                self.tb_move_or_delete_destination_dir,
            ],
            outputs=o_update_filter_and_gallery,
        ).then(**self.update_args)

        def delete_files(target_data: str, target_file: list[str], caption_ext: str):
            delete_img = "Image File" in target_file
            delete_txt = "Caption Text File" in target_file
            delete_bak = "Caption Backup File" in target_file
            if target_data == "Selected One":
                img_path = dataset_gallery.selected_path
                if img_path:
                    dte_instance.delete_dataset_file(
                        img_path, delete_img, caption_ext, delete_txt, delete_bak
                    )
                    dte_instance.construct_tag_infos()

            elif target_data == "All Displayed Ones":
                dte_instance.delete_dataset(
                    caption_ext, get_filters(), delete_img, delete_txt, delete_bak
                )

            return update_filter_and_gallery()

        self.btn_move_or_delete_delete_files.click(
            fn=delete_files,
            inputs=[
                self.rb_move_or_delete_target_data,
                self.cbg_move_or_delete_target_file,
                self.tb_move_or_delete_caption_ext,
            ],
            outputs=o_update_filter_and_gallery,
        ).then(**self.update_args)
