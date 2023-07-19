from modules import script_callbacks
from ui import ui_main
import gradio as gr

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        ui_main()
                    
        return [(ui_component, "纹样", "wenyang_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)
