from typing import get_type_hints
import gradio as gr

import settings


setting_inputs = {}
restore_funcs = {}


from i18n import i18n

def create_components():
    global setting_inputs
    th = get_type_hints(settings.Settings)

    for name, ty in th.items():
        s = getattr(settings.current, name)
        # i18n から名前(name)で翻訳を取得。なければ既存の説明文を使用
        label = i18n(name)
        if label == name:
            label = settings.DESCRIPTIONS.get(name, name)
            
        if ty is int or ty is float:
            if name == "single_tagger_default_threshold":
                elem = gr.Slider(value=s, label=label, minimum=0.0, maximum=1.0, step=0.01)
            else:
                elem = gr.Number(value=s, label=label)

            def restore(value):
                if name == "single_tagger_default_threshold":
                    return gr.Slider(value=value)
                return gr.Number(value=value)

        elif ty is bool:
            elem = gr.Checkbox(value=s, label=label)

            def restore(value):
                return gr.Checkbox(value=value)

        elif ty is str:
            if name == "ui_language":
                elem = gr.Dropdown(choices=["en", "jp"], value=s, label=label)
            elif name == "single_tagger_default_model":
                from tab_single_image import get_tagger_model_names
                elem = gr.Dropdown(choices=get_tagger_model_names(), value=s, label=label)
            else:
                elem = gr.Textbox(value=s, label=label)
            
            def restore(value):
                if name == "ui_language":
                    return gr.Dropdown(value=value)
                elif name == "single_tagger_default_model":
                    return gr.Dropdown(value=value)
                return gr.Textbox(value=value)

        else:
            raise NotImplementedError()
        setting_inputs[name] = elem
        restore_funcs[name] = restore


def on_ui_tabs():
    with gr.Row():
        btn_save = gr.Button(i18n("save_settings"), variant="primary")
        btn_restore = gr.Button(i18n("restore_defaults"))
    with gr.Column():
        create_components()
    
    btn_reload = gr.Button(i18n("reload_ui"), variant="primary", elem_id="reload_ui")

    def request_restart():
        from shared_state import state
        state.interrupt()
        state.restart()

    btn_reload.click(
        fn=request_restart,
        inputs=[],
        outputs=[],
    )

    def btn_save_clicked(inputs: dict):
        settings.current = settings.Settings(
            **{
                name: type(getattr(settings.current, name))(
                    inputs[setting_inputs[name]]
                )
                for name in settings.NAMES
            }
        )
        settings.save()

    btn_save.click(
        fn=btn_save_clicked,
        inputs={setting_inputs[name] for name in settings.NAMES},
    )

    def btn_restore_clicked():
        settings.restore_defaults()
        return {
            setting_inputs[name]: restore_funcs[name](getattr(settings.current, name))
            for name in settings.NAMES
        }

    btn_restore.click(fn=btn_restore_clicked, outputs=set(setting_inputs.values()))
