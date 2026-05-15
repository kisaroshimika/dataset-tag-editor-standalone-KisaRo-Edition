from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import gradio as gr

from .ui_common import *
from .uibase import UIBase
from .block_tag_select import TagSelectUI
from i18n import i18n

if TYPE_CHECKING:
    from .ui_classes import *

SortBy = dte_instance.SortBy
SortOrder = dte_instance.SortOrder


class BatchEditCaptionsUI(UIBase):
    def __init__(self):
        self.tag_select_ui_remove = TagSelectUI()
        self.show_only_selected_tags = False

    def create_ui(
        self, cfg_batch_edit, get_filters: Callable[[], list[dte_module.filters.Filter]]
    ):
        with gr.Tab(label=i18n("search_and_replace")):
            with gr.Column(variant="panel"):
                gr.HTML(i18n("edit_common_tags"))
                self.cb_show_only_tags_selected = gr.Checkbox(
                    value=cfg_batch_edit.show_only_selected,
                    label=i18n("show_only_positive"),
                )
                self.show_only_selected_tags = cfg_batch_edit.show_only_selected
                self.tb_common_tags = gr.Textbox(label=i18n("common_tags"), interactive=False)
                self.tb_edit_tags = gr.Textbox(label=i18n("edit_tags"), interactive=True)
                self.cb_prepend_tags = gr.Checkbox(
                    value=cfg_batch_edit.prepend, label=i18n("prepend_additional")
                )
                self.btn_apply_edit_tags = gr.Button(
                    value=i18n("apply_to_filtered"), variant="primary"
                )
                with gr.Accordion(
                    label=i18n("show_edit_description"), open=False
                ):
                    gr.HTML(
                        value="""
                    1. The tags common to all displayed images are shown in comma separated style.<br>
                    2. When changes are applied, all tags in each displayed images are replaced.<br>
                    3. If you change some tags into blank, they will be erased.<br>
                    4. If you add some tags to the end, they will be added to the end/beginning of the text file.<br>
                    5. Changes are not applied to the text files until the "Save all changes" button is pressed.<br>
                    <b>ex A.</b><br>
                    &emsp;Original Text = "A, A, B, C"&emsp;Common Tags = "B, A"&emsp;Edit Tags = "X, Y"<br>
                    &emsp;Result = "Y, Y, X, C"&emsp;(B->X, A->Y)<br>
                    <b>ex B.</b><br>
                    &emsp;Original Text = "A, B, C"&emsp;Common Tags = "(nothing)"&emsp;Edit Tags = "X, Y"<br>
                    &emsp;Result = "A, B, C, X, Y"&emsp;(add X and Y to the end (default))<br>
                    &emsp;Result = "X, Y, A, B, C"&emsp;(add X and Y to the beginning ("Prepend additional tags" checked))<br>
                    <b>ex C.</b><br>
                    &emsp;Original Text = "A, B, C, D, E"&emsp;Common Tags = "A, B, D"&emsp;Edit Tags = ", X, "<br>
                    &emsp;Result = "X, C, E"&emsp;(A->"", B->X, D->"")<br>
                    """
                    )
            with gr.Column(variant="panel"):
                gr.HTML(i18n("search_and_replace_displayed"))
                self.tb_sr_search_tags = gr.Textbox(
                    label=i18n("search_text"), interactive=True
                )
                self.tb_sr_replace_tags = gr.Textbox(
                    label=i18n("replace_text"), interactive=True
                )
                self.cb_use_regex = gr.Checkbox(
                    label=i18n("use_regex"), value=cfg_batch_edit.use_regex
                )
                self.rb_sr_replace_target = gr.Radio(
                    choices=[
                        (i18n("choice_only_selected_tags"), "Only Selected Tags"),
                        (i18n("choice_each_tags"), "Each Tags"),
                        (i18n("choice_entire_caption"), "Entire Caption"),
                    ],
                    value=cfg_batch_edit.target,
                    label=i18n("search_and_replace_in"),
                    interactive=True,
                )
                self.tb_sr_selected_tags = gr.Textbox(
                    label=i18n("selected_tags"), interactive=False, lines=2
                )
                self.btn_apply_sr_tags = gr.Button(
                    value=i18n("search_and_replace"), variant="primary"
                )
        with gr.Tab(label=i18n("remove")):
            with gr.Column(variant="panel"):
                gr.HTML(i18n("remove_duplicate_info"))
                self.btn_remove_duplicate = gr.Button(
                    value=i18n("remove_duplicate"), variant="primary"
                )
            with gr.Column(variant="panel"):
                gr.HTML(i18n("remove_selected_info"))
                self.btn_remove_selected = gr.Button(
                    value=i18n("remove_selected"), variant="primary"
                )
                self.tag_select_ui_remove.create_ui(
                    get_filters,
                    cfg_batch_edit.sory_by,
                    cfg_batch_edit.sort_order,
                    cfg_batch_edit.sw_prefix,
                    cfg_batch_edit.sw_suffix,
                    cfg_batch_edit.sw_regex,
                )
        with gr.Tab(label=i18n("extras")):
            with gr.Column(variant="panel"):
                gr.HTML(i18n("sort_displayed_info"))
                with gr.Row():
                    self.rb_sort_by = gr.Radio(
                        choices=[
                            (i18n("choice_alpha"), SortBy.ALPHA),
                            (i18n("choice_frequency"), SortBy.FREQ),
                            (i18n("choice_length"), SortBy.LEN),
                        ],
                        value=cfg_batch_edit.batch_sort_by,
                        interactive=True,
                        label=i18n("sort_by"),
                    )
                    self.rb_sort_order = gr.Radio(
                        choices=[
                            (i18n("choice_asc"), SortOrder.ASC),
                            (i18n("choice_desc"), SortOrder.DESC),
                        ],
                        value=cfg_batch_edit.batch_sort_order,
                        interactive=True,
                        label=i18n("sort_order"),
                    )
                self.btn_sort_selected = gr.Button(value=i18n("sort_tags"), variant="primary")
            with gr.Column(variant="panel"):
                gr.HTML(i18n("truncate_info"))
                self.nb_token_count = gr.Number(
                    value=cfg_batch_edit.token_count, precision=0
                )
                self.btn_truncate_by_token = gr.Button(
                    value=i18n("truncate_button"), variant="primary"
                )

    def set_callbacks(
        self,
        o_update_filter_and_gallery: list[gr.components.Component],
        load_dataset: LoadDatasetUI,
        filter_by_tags: FilterByTagsUI,
        get_filters: Callable[[], list[dte_module.filters.Filter]],
        update_filter_and_gallery: Callable[[], list],
    ):
        load_dataset.btn_load_datasets.click(
            fn=lambda: ["", ""], outputs=[self.tb_common_tags, self.tb_edit_tags]
        )

        def apply_edit_tags(search_tags: str, replace_tags: str, prepend: bool):
            search_tags = [t.strip() for t in search_tags.split(",")]
            search_tags = [t for t in search_tags if t]
            replace_tags = [t.strip() for t in replace_tags.split(",")]
            replace_tags = [t for t in replace_tags if t]

            dte_instance.replace_tags(
                search_tags=search_tags,
                replace_tags=replace_tags,
                filters=get_filters(),
                prepend=prepend,
            )
            filter_by_tags.tag_filter_ui.get_filter().tags = (
                dte_instance.get_replaced_tagset(
                    filter_by_tags.tag_filter_ui.get_filter().tags,
                    search_tags,
                    replace_tags,
                )
            )
            filter_by_tags.tag_filter_ui_neg.get_filter().tags = (
                dte_instance.get_replaced_tagset(
                    filter_by_tags.tag_filter_ui_neg.get_filter().tags,
                    search_tags,
                    replace_tags,
                )
            )

            return update_filter_and_gallery()

        self.btn_apply_edit_tags.click(
            fn=apply_edit_tags,
            inputs=[self.tb_common_tags, self.tb_edit_tags, self.cb_prepend_tags],
            outputs=o_update_filter_and_gallery,
        )
        self.btn_apply_edit_tags.click(
            fn=None, js="() => gl_dataset_images_close()"
        )

        def search_and_replace(
            search_text: str, replace_text: str, target_text: str, use_regex: bool
        ):
            if target_text == "Only Selected Tags":
                selected_tags = set(filter_by_tags.tag_filter_ui.selected_tags)
                dte_instance.search_and_replace_selected_tags(
                    search_text=search_text,
                    replace_text=replace_text,
                    selected_tags=selected_tags,
                    filters=get_filters(),
                    use_regex=use_regex,
                )
                filter_by_tags.tag_filter_ui.filter.tags = (
                    dte_instance.search_and_replace_tag_set(
                        search_text,
                        replace_text,
                        filter_by_tags.tag_filter_ui.filter.tags,
                        selected_tags,
                        use_regex,
                    )
                )
                filter_by_tags.tag_filter_ui_neg.filter.tags = (
                    dte_instance.search_and_replace_tag_set(
                        search_text,
                        replace_text,
                        filter_by_tags.tag_filter_ui_neg.filter.tags,
                        selected_tags,
                        use_regex,
                    )
                )

            elif target_text == "Each Tags":
                dte_instance.search_and_replace_selected_tags(
                    search_text=search_text,
                    replace_text=replace_text,
                    selected_tags=None,
                    filters=get_filters(),
                    use_regex=use_regex,
                )
                filter_by_tags.tag_filter_ui.filter.tags = (
                    dte_instance.search_and_replace_tag_set(
                        search_text,
                        replace_text,
                        filter_by_tags.tag_filter_ui.filter.tags,
                        None,
                        use_regex,
                    )
                )
                filter_by_tags.tag_filter_ui_neg.filter.tags = (
                    dte_instance.search_and_replace_tag_set(
                        search_text,
                        replace_text,
                        filter_by_tags.tag_filter_ui_neg.filter.tags,
                        None,
                        use_regex,
                    )
                )

            elif target_text == "Entire Caption":
                dte_instance.search_and_replace_caption(
                    search_text=search_text,
                    replace_text=replace_text,
                    filters=get_filters(),
                    use_regex=use_regex,
                )
                filter_by_tags.tag_filter_ui.filter.tags = (
                    dte_instance.search_and_replace_tag_set(
                        search_text,
                        replace_text,
                        filter_by_tags.tag_filter_ui.filter.tags,
                        None,
                        use_regex,
                    )
                )
                filter_by_tags.tag_filter_ui_neg.filter.tags = (
                    dte_instance.search_and_replace_tag_set(
                        search_text,
                        replace_text,
                        filter_by_tags.tag_filter_ui_neg.filter.tags,
                        None,
                        use_regex,
                    )
                )

            return update_filter_and_gallery()

        self.btn_apply_sr_tags.click(
            fn=search_and_replace,
            inputs=[
                self.tb_sr_search_tags,
                self.tb_sr_replace_tags,
                self.rb_sr_replace_target,
                self.cb_use_regex,
            ],
            outputs=o_update_filter_and_gallery,
        )
        self.btn_apply_sr_tags.click(
            fn=None, js="() => gl_dataset_images_close()"
        )

        def cb_show_only_tags_selected_changed(value: bool):
            self.show_only_selected_tags = value
            return self.get_common_tags(get_filters, filter_by_tags)

        self.cb_show_only_tags_selected.change(
            fn=cb_show_only_tags_selected_changed,
            inputs=self.cb_show_only_tags_selected,
            outputs=[self.tb_common_tags, self.tb_edit_tags],
        )

        def remove_duplicated_tags():
            dte_instance.remove_duplicated_tags(get_filters())
            return update_filter_and_gallery()

        self.btn_remove_duplicate.click(
            fn=remove_duplicated_tags, outputs=o_update_filter_and_gallery
        )

        self.tag_select_ui_remove.set_callbacks()

        def remove_selected_tags():
            dte_instance.remove_tags(
                self.tag_select_ui_remove.selected_tags, get_filters()
            )
            return update_filter_and_gallery()

        self.btn_remove_selected.click(
            fn=remove_selected_tags, outputs=o_update_filter_and_gallery
        )

        def sort_selected_tags(sort_by: str, sort_order: str):
            sort_by = SortBy(sort_by)
            sort_order = SortOrder(sort_order)
            dte_instance.sort_filtered_tags(
                get_filters(), sort_by=sort_by, sort_order=sort_order
            )
            return update_filter_and_gallery()

        self.btn_sort_selected.click(
            fn=sort_selected_tags,
            inputs=[self.rb_sort_by, self.rb_sort_order],
            outputs=o_update_filter_and_gallery,
        )

        self.cb_show_only_tags_selected.change(
            fn=self.func_to_set_value("show_only_selected_tags"),
            inputs=self.cb_show_only_tags_selected,
        )

        def truncate_by_token_count(token_count: int):
            token_count = max(int(token_count), 0)
            dte_instance.truncate_filtered_tags_by_token_count(
                get_filters(), token_count
            )
            return update_filter_and_gallery()

        self.btn_truncate_by_token.click(
            fn=truncate_by_token_count,
            inputs=self.nb_token_count,
            outputs=o_update_filter_and_gallery,
        )

    def get_common_tags(
        self,
        get_filters: Callable[[], list[dte_module.filters.Filter]],
        filter_by_tags: FilterByTagsUI,
    ):
        if self.show_only_selected_tags:
            tags = ", ".join(
                [
                    t
                    for t in dte_instance.get_common_tags(filters=get_filters())
                    if t in filter_by_tags.tag_filter_ui.filter.tags
                ]
            )
        else:
            tags = ", ".join(dte_instance.get_common_tags(filters=get_filters()))
        return [tags, tags]
