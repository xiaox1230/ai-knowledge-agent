import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import os

# 加载环境变量
load_dotenv()

# DeepSeek客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 页面标题
st.title("AI知识库助手")

# 上传PDF
uploaded_file = st.file_uploader(
    "上传PDF文件",
    type=["pdf"]
)

# 用户问题
question = st.text_input("请输入你的问题")

# 按钮
if st.button("开始提问"):

    # 判断是否上传文件
    if uploaded_file and question:

        with st.spinner("AI思考中..."):

            # 读取PDF
            pdf_reader = PdfReader(uploaded_file)

            # 存储PDF文本
            pdf_text = ""

            # 遍历每一页
            for page in pdf_reader.pages:

                # 提取文本
                text = page.extract_text()

                # 防止空页报错
                if text:
                    pdf_text += text

            # 构建Prompt
            prompt = f"""
            你是一个专业的知识库AI助手。

            以下是PDF文档内容：

            {pdf_text}

            用户问题：
            {question}

            请根据PDF内容准确回答。
            如果文档中没有相关内容，请明确说明。
            """

            # 调用AI
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )

            # 获取结果
            result = response.choices[0].message.content

            # 显示结果
            st.success("回答完成")

            st.write(result)

    else:

        st.warning("请上传PDF并输入问题")