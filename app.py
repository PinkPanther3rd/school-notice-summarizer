import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="学校お知らせまとめ",
    page_icon="📚",
    layout="centered"
)

st.title("📚 学校お知らせ AIまとめ")
st.subheader("スマホで簡単まとめツール")

notice_text = st.text_area(
    "学校アプリからお知らせをコピーしてここに貼り付けてください",
    height=250,
    placeholder="令和... 保護者各位...\n提出物：...など"
)

if st.button("📋 要約する", type="primary", use_container_width=True):
    if not notice_text.strip():
        st.error("お知らせを貼り付けてください")
    else:
        with st.spinner("AIがまとめています..."):
            # 簡易要約（後で本格LLMに強化可能）
            lines = notice_text.strip().split('\n')[:10]  # 最初の10行を例に
            summary = f"""
### {datetime.now().strftime('%Y年%m月%d日 %H:%M')} のまとめ

**重要ポイント**
- 詳細は原文を確認してください
- 提出物や期限がある場合は早めに準備を

**内容概要**
{notice_text[:300]}...

**次のアクション**
• カレンダーに予定を登録
• 必要なものは準備
            """
            st.success("✅ まとめ完了！")
            st.markdown(summary)
            
            # コピーしやすいように
            st.text_area("コピー用", summary, height=200)

st.caption("Made for 学校お知らせまとめ | スマホ対応")
