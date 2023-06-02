import modules.scripts as scripts
import gradio as gr
import os

from modules import script_callbacks

with gr.Blocks() as tab1:
    with gr.Row():
        with gr.Column():
            d1 = gr.Dropdown(choices=['龙', '凤'], label='纹样图片类型')
            d2 = gr.Dropdown(choices=['原始纹样', '生成纹样'])
            t1 = gr.Textbox(label='纹样描述')
        image1 = gr.Image(type="pil")
    b1 = gr.Button('查询')
    gallery = gr.Gallery(label="符合查询条件的图片").style(columns=[2], rows=[2], object_fit="contain", height="auto")
    b2 = gr.Button('确认选中图片，跳转至训练')

def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths

with gr.Blocks() as tab2:
    with gr.Row():
        with gr.Column():
            file_output = gr.File()
            upload_button = gr.UploadButton("上传训练图片", file_types=["image"], file_count="multiple")
        with gr.Column():
            d1 = gr.Dropdown(choices=['lora', 'dreambooth', 'embedding'])
            t1 = gr.Textbox(label='params')
            b1 = gr.Button('开始训练')
            b2 = gr.Button('跳转至训练模块，配置更多参数')
        with gr.Column():
            p1 = gr.Textbox('progess')
            t2 = gr.Textbox('模型名称')
            b2 = gr.Button('保存模型')
    with gr.Row():
        with gr.Column():
            d1 = gr.Dropdown(label='选择模型', choices=['龙纹样模型', '凤纹样模型', 'xxx'])
            t1 = gr.Textbox(label='params')
            b1 = gr.Button('开始生成')
            b2 = gr.Button('跳转至生成模块，配置更多参数')
        gallery = gr.Gallery(label="生成的图片").style(columns=[2], rows=[2], object_fit="contain",
                                                               height="auto")
    with gr.Row():
        t2 = gr.Textbox(label='纹样图片类型')
        b2 = gr.Button('确认保存')

with gr.Blocks() as tab3:
    with gr.Row():
        with gr.Column(scale=1):
            t1 = gr.Textbox(label='纹样图片网址')
            b1 = gr.Button('添加网址')
            b1 = gr.Button('删除选中网址')
            d1 = gr.Dropdown(choices=['tuku.baidi.com', 'xxx.com'], label='已添加的网址')
            with gr.Box():
                b11 = gr.Button('查看爬取的图片')
                gallery = gr.Gallery(label="爬取的图片").style(columns=[2], rows=[2], object_fit="contain", height="auto")

        with gr.Column(scale=1):
            file_output = gr.File()
            upload_button = gr.UploadButton("批量上传纹样图片", file_types=["image"], file_count="multiple")
            upload_button.upload(upload_file, upload_button, file_output)
            t2 = gr.Textbox(label='纹样图片类型')
            b2 = gr.Button('确认保存')

with gr.Blocks() as tab4:
    t = gr.Textbox()

tabss = [
    (tab1, "纹样查看"),
    (tab2, '训练和生成'),
    (tab3, '纹样存储'),
    (tab4, '导出XR')
]

# with gr.Blocks(mode="LLC", title="llc") as demo:
#     gr.Markdown("纹样平台")
#     with gr.Tabs() as tabs:
#         for tab, label in tabss:
#             with gr.TabItem(label):
#                 tab.render()
# demo.launch()

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        gr.Markdown("纹样平台")
        with gr.Tabs() as tabs:
            for tab, label in tabss:
                with gr.TabItem(label):
                    tab.render()
                    
        return [(ui_component, "纹样", "wenyang_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)
