from typing import Callable
import gradio as gr

from .ui_common import *
from i18n import i18n

TagFilter = dte_module.filters.TagFilter
Filter = dte_module.filters.Filter

SortBy = dte_instance.SortBy
SortOrder = dte_instance.SortOrder


class TagSelectUI:
    def __init__(self):
        self.filter_word = ""
        self.sort_by = SortBy.ALPHA
        self.sort_order = SortOrder.ASC
        self.selected_tags = set()
        self.tags = set()
        self.get_filters = lambda: []
        self.prefix = False
        self.suffix = False
        self.regex = False

    def create_ui(
        self,
        get_filters: Callable[[], list[Filter]],
        sort_by=SortBy.ALPHA,
        sort_order=SortOrder.ASC,
        prefix=False,
        suffix=False,
        regex=False,
    ):
        self.get_filters = get_filters
        self.prefix = prefix
        self.suffix = suffix
        self.regex = regex

        self.tb_search_tags = gr.Textbox(label=i18n("search_tags"), interactive=True)
        with gr.Row():
            self.cb_prefix = gr.Checkbox(label=i18n("prefix"), value=False, interactive=True)
            self.cb_suffix = gr.Checkbox(label=i18n("suffix"), value=False, interactive=True)
            self.cb_regex = gr.Checkbox(
                label=i18n("use_regex"), value=False, interactive=True
            )
        with gr.Row():
            self.rb_sort_by = gr.Radio(
                choices=[
                    (i18n("choice_alpha"), SortBy.ALPHA),
                    (i18n("choice_frequency"), SortBy.FREQ),
                    (i18n("choice_length"), SortBy.LEN),
                ],
                value=sort_by,
                interactive=True,
                label=i18n("sort_by"),
            )
            self.rb_sort_order = gr.Radio(
                choices=[
                    (i18n("choice_asc"), SortOrder.ASC),
                    (i18n("choice_desc"), SortOrder.DESC),
                ],
                value=sort_order,
                interactive=True,
                label=i18n("sort_order"),
            )
        with gr.Row():
            self.btn_select_visibles = gr.Button(value=i18n("select_visible"))
            self.btn_deselect_visibles = gr.Button(value=i18n("deselect_visible"))
        self.cbg_tags = gr.CheckboxGroup(label=i18n("select_tags"), interactive=True)

    def set_callbacks(self):
        o_update = self.cbg_tags
        self.tb_search_tags.change(
            fn=self.tb_search_tags_changed,
            inputs=self.tb_search_tags
        ).then(
            fn=self.cbg_tags_update, outputs=o_update
        )
        self.cb_prefix.change(
            fn=self.cb_prefix_changed, inputs=self.cb_prefix, outputs=o_update
        )
        self.cb_suffix.change(
            fn=self.cb_suffix_changed, inputs=self.cb_suffix, outputs=o_update
        )
        self.cb_regex.change(
            fn=self.cb_regex_changed, inputs=self.cb_regex, outputs=o_update
        )
        self.rb_sort_by.change(
            fn=self.rd_sort_by_changed, inputs=self.rb_sort_by, outputs=o_update
        )
        self.rb_sort_order.change(
            fn=self.rd_sort_order_changed,
            inputs=self.rb_sort_order,
            outputs=o_update,
        )
        self.btn_select_visibles.click(
            fn=self.btn_select_visibles_clicked, outputs=o_update
        )
        self.btn_deselect_visibles.click(
            fn=self.btn_deselect_visibles_clicked,
            inputs=self.cbg_tags,
            outputs=o_update,
        )
        self.cbg_tags.change(
            fn=self.cbg_tags_changed, inputs=self.cbg_tags, outputs=o_update
        )

    def tb_search_tags_changed(self, tb_search_tags: str):
        self.filter_word = tb_search_tags

    def cb_prefix_changed(self, prefix: bool):
        self.prefix = prefix
        return self.cbg_tags_update()

    def cb_suffix_changed(self, suffix: bool):
        self.suffix = suffix
        return self.cbg_tags_update()

    def cb_regex_changed(self, regex: bool):
        self.regex = regex
        return self.cbg_tags_update()

    def rd_sort_by_changed(self, rb_sort_by: str):
        self.sort_by = rb_sort_by
        return self.cbg_tags_update()

    def rd_sort_order_changed(self, rd_sort_order: str):
        self.sort_order = rd_sort_order
        return self.cbg_tags_update()

    def cbg_tags_changed(self, cbg_tags: list[str]):
        self.selected_tags = set(dte_instance.read_tags(cbg_tags))
        return self.cbg_tags_update()

    def btn_deselect_visibles_clicked(self, cbg_tags: list[str]):
        tags = dte_instance.get_filtered_tags(
            self.get_filters(), self.filter_word, True
        )
        selected_tags = set(dte_instance.read_tags(cbg_tags)) & tags
        self.selected_tags -= selected_tags
        return self.cbg_tags_update()

    def btn_select_visibles_clicked(self):
        tags = set(
            dte_instance.get_filtered_tags(self.get_filters(), self.filter_word, True)
        )
        self.selected_tags |= tags
        return self.cbg_tags_update()

    def cbg_tags_update(self):
        tags = dte_instance.get_filtered_tags(
            self.get_filters(),
            self.filter_word,
            True,
            prefix=self.prefix,
            suffix=self.suffix,
            regex=self.regex,
        )
        self.tags = set(
            dte_instance.get_filtered_tags(
                self.get_filters(),
                filter_tags=True,
                prefix=self.prefix,
                suffix=self.suffix,
                regex=self.regex,
            )
        )
        self.selected_tags &= self.tags
        tags = dte_instance.sort_tags(
            tags=tags, sort_by=self.sort_by, sort_order=self.sort_order
        )
        tags = dte_instance.write_tags(tags, self.sort_by)
        selected_tags = dte_instance.write_tags(list(self.selected_tags), self.sort_by)
        return gr.CheckboxGroup(value=selected_tags, choices=tags)
