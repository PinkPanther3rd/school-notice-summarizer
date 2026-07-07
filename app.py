import streamlit as st
from datetime import datetime

st.set_page_config(page_title="学校お知らせまとめ", layout="centered")

st.title("📚 学校お知らせ AIまとめ")
st.subheader("日々のお知らせを整理")

# セッション状態
if "notices" not in st.session_state:
    st.session_state.notices = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 入力エリア
col1, col2 = st.columns([3, 1])
with col1:
    notice_text = st.text_area(
        "新しいお知らせをここに貼り付けてください",
        height=180,
        placeholder="令和... 保護者各位...",
        key="notice_input"
    )
with col2:
    date_str = st.text_input("日付", value=datetime.now().strftime("%Y-%m-%d"))
    title = st.text_input("タイトル（任意）", placeholder="例：提出物のお知らせ")

if st.button("✅ 追加して要約", type="primary", use_container_width=True):
    if notice_text.strip():
        summary = notice_text[:200] + "..." if len(notice_text) > 200 else notice_text
        
        new_notice = {
            "date": date_str,
            "title": title or "無題のお知らせ",
            "summary": summary,
            "full_text": notice_text,
            "timestamp": datetime.now().isoformat()
        }
        
        st.session_state.notices.append(new_notice)
        
        # タスク抽出
        task_keywords = ["提出", "期限", "持参", "準備", "宿題", "提出物"]
        if any(kw in notice_text for kw in task_keywords):
            st.session_state.tasks.append({
                "date": date_str,
                "task": title or "確認が必要なタスク",
                "detail": notice_text[:120]
            })
        
        st.success("✅ 追加しました！ 次のお知らせをどうぞ")
        
        # 入力欄クリア（正しい方法）
        st.rerun()
        
    else:
        st.error("お知らせを入力してください")

# 表示部分
tab1, tab2 = st.tabs(["📋 お知らせリスト", "✅ タスクリスト"])

with tab1:
    if st.session_state.notices:
        for notice in reversed(st.session_state.notices):
            with st.expander(f"📅 {notice['date']} - {notice['title']}"):
                st.write("**要約:**")
                st.write(notice['summary'])
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

st.caption("※ ブラウザを閉じるとデータは消えます")
