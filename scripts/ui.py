import gradio as gr
import db
from PIL import Image

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
                gallery = gr.Gallery(label="爬取的图片").style(columns=[2], rows=[2], object_fit="contain",
                                                               height="auto")

        with gr.Column(scale=1):
            file_output = gr.File()
            upload_button = gr.UploadButton("批量上传纹样图片", file_types=["image"], file_count="multiple")
            upload_button.upload(upload_file, upload_button, file_output)
            t2 = gr.Textbox(label='纹样图片类型')
            b2 = gr.Button('确认保存')

with gr.Blocks() as tab4:
    t = gr.Textbox()

def query(period, content, race, isAI):
    result = db.query(period, content, race, isAI)
    imgs = []
    for r in result:
        imgs.append(Image.open(f"{db.img_save_dir()}/{r[0]}"))

    print(f"query image size: {len(imgs)}")
    return imgs
def upload(files):
    file_paths = [file.name for file in files]
    return file_paths

def save_image(images, period, content, race, isAI):
    for img in images:
        try:
            img_ = Image.open(img.name)
            img_.convert("RGB").save(f"{db.img_save_dir()}/{img.orig_name}")
            db.insertWenyang([(period, content, race, isAI, img.orig_name)])
        except Exception as e:
            print(e)

    period_new = db.queryType('period')
    if period not in period_new:
        period_new.append(period)

    content_new = db.queryType('content')
    if content not in content_new:
        content_new.append(content)

    return [gr.Dropdown.update(choices=period_new), gr.Dropdown.update(choices=content_new)]

css = """
#box_style {border-color: #FFCCCB} 
"""

with gr.Blocks() as tab5:
    with gr.Row():
        with gr.Column(scale=10):
            with gr.Box():
                gr.Markdown("""
                    ###                  <center>查 询</center>
                    """)
                with gr.Row():
                    d1 = gr.Dropdown(choices=db.queryType('period'), label='朝代')
                    d2 = gr.Dropdown(choices=db.queryType('content'), label='图案类型')
                    d3 = gr.Dropdown(choices=[], label='民族')
                    d4 = gr.Dropdown(choices=['是', '否'], label='是否AI生成')
                b1 = gr.Button('查询纹样')

                gallery = gr.Gallery(label="符合查询条件的图片")
                # b2 = gr.Button('下一页')

                b1.click(query, [d1, d2, d3, d4], gallery)
        with gr.Column(scale=1, min_width=5):
            gr.HTML()
        with gr.Column(scale=10):
            with gr.Box(elem_id="box_style"):
                gr.Markdown("""
                                    ###                  <center>导 入</center>
                                    """)
                file_output = gr.File(file_count="multiple", type="file", label="原始图片")
                t2 = gr.Textbox(label='朝代')
                t3 = gr.Textbox(label='图案类型')
                t4 = gr.Textbox(label='民族')
                d11 = gr.Dropdown(label='是否AI生成', choices=['是', '否'])
                b2 = gr.Button('确认保存')

                b2.click(save_image, [file_output, t2, t3, t4, d11], [d1, d2])

def save_config(config):
    1

with gr.Blocks() as tab6:
    t = gr.Textbox(label='纹样数据的存储路径')
    b = gr.Button(label='配置生效')
    b.click(save_config, t)

tabss = [
    # (tab1, "纹样查看"),
    # (tab2, '训练和生成'),
    # (tab3, '纹样存储'),
    (tab5, '纹样数据库'),
    # (tab4, '导出XR'),
    # (tab6, '系统设置')
]


def ui_main():
    gr.Markdown("""
    # 纹样平台
    """)
    with gr.Tabs() as tabs:
        for tab, label in tabss:
            with gr.TabItem(label):
                tab.render()

with gr.Blocks(mode="LLC", title="llc") as demo:
    ui_main()


demo.launch(share=db.args.share)
