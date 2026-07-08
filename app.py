import streamlit as st
from datetime import datetime
import PyPDF2
from io import BytesIO

st.set_page_config(page_title="学校お知らせまとめ", layout="centered")

st.title("📚 学校お知らせ AIまとめ")
st.subheader("テキスト・PDF対応")

# セッション状態
if "notices" not in st.session_state:
    st.session_state.notices = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 入力方法選択
input_method = st.radio("入力方法を選択", ["テキスト貼り付け", "PDFアップロード"])

if input_method == "テキスト貼り付け":
    notice_text = st.text_area(
        "お知らせを貼り付けてください",
        height=150,
        placeholder="令和..."
    )
else:  # PDF
    uploaded_file = st.file_uploader("PDFファイルを選択", type="pdf")
    notice_text = ""
    if uploaded_file:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                notice_text += page.extract_text() + "\n"
            st.success(f"PDFから {len(notice_text)}文字 抽出しました")
        except:
            st.error("PDFの読み込みに失敗しました")

# 共通入力
col1, col2 = st.columns([3, 1])
with col1:
    title = st.text_input("タイトル（任意）", placeholder="例：8月提出物")
with col2:
    date_str = st.text_input("日付", value=datetime.now().strftime("%Y-%m-%d"))

if st.button("✅ 追加して要約", type="primary", use_container_width=True):
    if notice_text.strip():
        summary = notice_text[:250] + "..." if len(notice_text) > 250 else notice_text
        
        new_notice = {
            "date": date_str,
            "title": title or "無題のお知らせ",
            "summary": summary,
            "full_text": notice_text,
            "timestamp": datetime.now().isoformat(),
            "source": "PDF" if input_method == "PDFアップロード" else "テキスト"
        }
        
        st.session_state.notices.append(new_notice)
        
        # タスク抽出
        task_keywords = ["提出", "期限", "持参", "準備", "宿題", "提出物", "締切"]
        if any(kw in notice_text for kw in task_keywords):
            st.session_state.tasks.append({
                "date": date_str,
                "task": title or "確認が必要",
                "detail": notice_text[:150]
            })
        
        st.success("追加しました！")
        st.rerun()
    else:
        st.error("内容を入力またはPDFをアップロードしてください")

# 表示部分（前回と同じ）
tab1, tab2 = st.tabs(["📋 お知らせリスト", "✅ タスクリスト"])

with tab1:
    if st.session_state.notices:
        for notice in reversed(st.session_state.notices):
            with st.expander(f"📅 {notice['date']} - {notice['title']} ({notice.get('source','')})"):
                st.write("**要約:**", notice['summary'])
                st.write("---")
                st.write("**原文:**")
                st.write(notice['full_text'])
    else:
        st.info("まだお知らせがありません")

with tab2:
    if st.session_state.tasks:
        st.subheader("やるべきこと")
        for task in reversed(st.session_state.tasks):
            st.warning(f"**{task['date']}** {task['task']}\n\n{task['detail']}")
    else:
        st.info("現在タスクはありません")

st.caption("PDF対応版 | データはブラウザを閉じると消えます")
