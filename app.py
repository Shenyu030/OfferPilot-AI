from pypdf import PdfReader
from docx import Document
from dashscope import Generation
import streamlit as st

# 请替换成你自己的 API Key，或者从环境变量读取
# import os
# dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

def test_ai():
    """测试 AI 连接"""
    response = Generation.call(
        model="qwen-turbo",
        prompt="请用一句话介绍杭州"
    )
    return response.output.text

def optimize_resume(resume_text):
    """简历优化"""
    prompt = f"""
你是一位资深互联网HR和AI行业招聘专家。

请优化下面这份简历。

要求：

1. 保留真实经历，不允许编造
2. 表达更专业
3. 更符合AI产品、AI应用开发、数据分析相关岗位
4. 突出项目经历和成果
5. 输出优化后的完整内容

简历内容：

{resume_text}
"""
    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt
    )
    return response.output.text

def read_pdf(file):
    """读取 PDF 文件"""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def read_docx(file):
    """读取 DOCX 文件"""
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def analyze_match(resume_text, jd_text):
    """岗位匹配分析"""
    prompt = f"""
你是一位资深AI招聘顾问。

请根据候选人简历和岗位JD进行分析。

输出格式：

## 匹配度
给出0-100分

## 候选人优势
列出3-5条

## 候选人短板
列出3-5条

## 提升建议
给出具体行动建议

================

候选人简历：

{resume_text}

================

岗位JD：

{jd_text}
"""
    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt
    )
    return response.output.text

def generate_learning_plan(target_role):

    prompt = f"""
你是一位AI职业发展导师。

用户目标岗位：

{target_role}

请输出：

# 岗位核心能力

# 当前应重点掌握的技能

# 30天学习路线

按照：

第1周
第2周
第3周
第4周

输出。

最后补充：

# 推荐项目练习
"""

    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt
    )

    return response.output.text

# ========== Streamlit UI ==========
st.set_page_config(page_title="AI求职助手", layout="centered")
st.title("🚀 OfferPilot AI")
st.markdown("""
### AI求职成长助手

帮助求职者完成：

✅ 简历优化

✅ 岗位匹配分析

✅ 学习路线规划

✅ 简历文件解析

基于通义千问大模型驱动
""")
st.subheader("简历优化 / JD分析 / 面试生成")

if st.button("测试AI连接"):
    result = test_ai()
    st.write(result)

# 选择功能
mode = st.selectbox(
    "请选择功能",
    [ "简历优化",
    "岗位匹配分析",
    "学习路线规划",
    "面试题生成（模拟版）"]
)

st.divider()

# ========== 简历优化功能 ==========
if mode == "简历优化":
    uploaded_file = st.file_uploader(
        "上传简历（PDF或Word）",
        type=["pdf", "docx"]
    )

    resume_text = ""   # 用于存储提取的简历文本

    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = read_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            resume_text = read_docx(uploaded_file)
        st.success("简历读取成功")

        # 显示可编辑的文本区域
        resume_text = st.text_area(
            "识别结果（可修改）",
            value=resume_text,
            height=300
        )
    else:
        resume_text = st.text_area(
            "请输入简历内容",
            height=300,
            placeholder="把你的简历内容粘贴到这里..."
        )

    if st.button("开始优化"):
        if resume_text.strip() == "":
            st.warning("请先输入简历内容")
        else:
            with st.spinner("AI正在优化简历，请稍候..."):
                result = optimize_resume(resume_text)
            st.success("优化完成")
            st.download_button(
                "下载优化结果",
                result,
                file_name="optimized_resume.txt"
            )
            st.markdown(result)

# ========== 岗位匹配分析 ==========
elif mode == "岗位匹配分析":
    resume_for_match = st.text_area(
        "请输入你的简历",
        height=200
    )
    jd = st.text_area(
        "请输入岗位JD",
        height=200
    )

    if st.button("开始分析"):
        if resume_for_match.strip() == "":
            st.warning("请先输入简历")
        elif jd.strip() == "":
            st.warning("请先输入岗位JD")
        else:
            with st.spinner("AI正在分析匹配度..."):
                result = analyze_match(resume_for_match, jd)
            st.success("分析完成")
            st.markdown(result)

elif mode == "学习路线规划":

    target_role = st.text_input(
        "请输入目标岗位"
    )

    if st.button("生成学习路线"):

        if target_role.strip() == "":
            st.warning("请输入目标岗位")

        else:

            with st.spinner("AI正在规划学习路线..."):

                result = generate_learning_plan(
                    target_role
                )

            st.success("规划完成")

            st.markdown(result)

# ========== 面试题生成（模拟版） ==========
elif mode == "面试题生成（模拟版）":
    role = st.text_input("请输入岗位名称（如：AI工程师 / 产品助理）")
    if st.button("生成面试题"):
        if role.strip() == "":
            st.warning("请先输入岗位名称")
        else:
            st.success("面试题（模拟生成）")
            st.write(f"""
### {role} 常见面试问题

1. 你为什么选择这个方向？
2. 介绍一下你做过的项目
3. 你如何理解这个岗位的核心能力？
4. 如果让你做一个XX产品，你会怎么设计？
5. 你最大的挑战是什么？

👉（后续版本会用AI动态生成）
""")

st.divider()
st.caption("Day 1版本：仅用于构建产品框架，未接入AI模型")