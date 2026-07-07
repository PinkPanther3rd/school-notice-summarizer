import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="学校お知らせまとめ", layout="centered")

st.title("📚 学校お知らせ AIまとめ")
st.subheader("日々のお知らせを整理")

# セッション状態の初期化
if "notices" not in st.session_state:
    st.session_state.notices = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 新しいお知らせ入力
notice_text = st.text_area(
    "新しいお知らせをここに貼り付けてください",
    height=200,
    placeholder="令和... 保護者各位... 提出物..."
)

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("お知らせのタイトル（任意）", placeholder="例：8月提出物のお知らせ")
with col2:
    date_str = st.text_input("日付（任意）", value=datetime.now().strftime("%Y-%m-%d"))

if st.button("✅ 追加して要約", type="primary", use_container_width=True):
    if notice_text.strip():
        summary = f"要約：{notice_text[:150]}..."  # 簡易要約（後で強化）
        
        new_notice = {
            "date": date_str,
            "title": title or "無題のお知らせ",
            "summary": summary,
            "full_text": notice_text,
            "timestamp": datetime.now().isoformat()
        }
        
        st.session_state.notices.append(new_notice)
        
        # 簡易タスク抽出
        if any(word in notice_text for word in ["提出", "期限", "持参", "準備", "宿題"]):
            st.session_state.tasks.append({
                "date": date_str,
                "task": title or "要確認タスク",
                "detail": notice_text[:100]
            })
        
        st.success("追加しました！")
    else:
        st.error("お知らせを入力してください")

# 表示部分
tab1, tab2 = st.tabs(["📋 お知らせリスト", "✅ タスクリスト"])

with tab1:
    if st.session_state.notices:
        for notice in reversed(st.session_state.notices):
            with st.expander(f"📅 {notice['date']} - {notice['title']}"):
                st.write(notice['summary'])
                if st.button("詳細を見る", key=notice['timestamp']):
                    st.write(notice['full_text'])
    else:
        st.info("まだお知らせがありません")

with tab2:
    if st.session_state.tasks:
        for task in st.session_state.tasks:
            st.warning(f"**{task['date']}** {task['task']}\n\n{task['detail']}")
    else:
        st.info("現在タスクはありません")

st.caption("※ ブラウザを閉じるとデータが消えます（後で保存機能追加可能）")
