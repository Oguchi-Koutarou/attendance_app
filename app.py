import streamlit as st
from datetime import datetime, timedelta, timezone
import requests

# ★GASのURL
GAS_URL = "https://script.google.com/macros/s/AKfycbxmYi3zgPNbPqovN-99kbnTQjrczsXfvRxWF4GG2OA916UyFvyCDqJM-7gWI6Qj7JyMbg/exec"

# セッション状態の初期化
if "page" not in st.session_state:
    st.session_state["page"] = "user"
if "admin_auth" not in st.session_state:
    st.session_state["admin_auth"] = False

# ==========================================
# 1. 管理者用ページ
# ==========================================
if st.session_state["page"] == "admin":
    st.title("🔒 管理者ログイン")
    if not st.session_state["admin_auth"]:
        admin_pass = st.text_input("管理者用パスワードを入力してください", type="password")
        if st.button("ログイン"):
            if admin_pass == "converter":
                st.session_state["admin_auth"] = True
                st.rerun()
            else:
                st.error("⚠️ パスワードが間違っています。")
        st.write("---")
        if st.button("← アンケート回答ページに戻る"):
            st.session_state["page"] = "user"
            st.rerun()
    else:
        st.title("📊 管理者専用ページ")
        st.success("管理者としてログインしました。")
        st.link_button("📊 Googleスプレッドシートを開く", "https://docs.google.com/spreadsheets/u/0/")
        st.write("---")
        if st.button("ログアウト"):
            st.session_state["admin_auth"] = False
            st.session_state["page"] = "user"
            st.rerun()

# ==========================================
# 2. 回答者用ページ
# ==========================================
elif st.session_state["page"] == "user":
    st.title("TMU Annual Research Forum")
    
    name_kanji = st.text_input("お名前（漢字） *")
    name_furigana = st.text_input("お名前（ふりがな） *")

    st.subheader("2. 参加の確認")
    attendance_status = st.radio("イベントへの参加について", ["参加", "不参加"])

    days_choice, friday_party, saturday_party = "ー", "ー", "ー"
    occupation, affiliation = "ー", "ー"
    ob_cooperation, prof_cooperation, student_presentation = "ー", "ー", "ー"
    message = "" # 追加

    if attendance_status == "参加":
        st.markdown("---")
        st.subheader("3. 参加日程について")
        days_choice = st.radio("参加日程 *", ["両日参加", "金曜（11/13）のみ参加", "土曜（11/14）のみ参加"])
        
        st.markdown("---")
        st.subheader("4. 懇親会について")
        friday_party = st.radio("金曜夜の懇親会", ["参加", "不参加"])
        saturday_party = st.radio("土曜夜の懇親会", ["参加", "不参加"])
        
        st.markdown("---")
        st.subheader("5. 所属・職業")
        occupation = st.selectbox("職業 *", ["学生", "教員", "企業", "その他"])
        affiliation = st.text_input("学校名または会社名 *")

        if occupation == "企業":
            ob_cooperation = st.radio("OBからの会社紹介（15分程度）へご協力していただけますか？", ["はい", "いいえ"])
        elif occupation == "教員":
            prof_cooperation = st.radio("研究室紹介にご協力いただけますか？", ["はい", "いいえ"])
        elif occupation == "学生":
            student_presentation = st.radio("2日目にポスター形式にて研究発表を予定しています。発表しますか？", ["はい", "いいえ"])

    # メッセージ入力欄（任意）
    st.markdown("---")
    st.subheader("6. ひと言メッセージ")
    message = st.text_area("何かメッセージがあればご記入ください")

    st.markdown("---")
    if st.button("回答を送信する", type="primary"):
        if not name_kanji or not name_furigana or (attendance_status == "参加" and not affiliation):
            st.warning("⚠️ 必須項目を入力してください。")
        else:
            jst = timezone(timedelta(hours=9))
            jst_now = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")

            payload = {
                "日時": jst_now,
                "お名前漢字": name_kanji,
                "お名前ふりがな": name_furigana,
                "出欠": attendance_status,
                "参加日程": days_choice,
                "金曜懇親会": friday_party,
                "土曜懇親会": saturday_party,
                "職業": occupation,
                "所属名": affiliation,
                "OB協力": ob_cooperation,
                "教員協力": prof_cooperation,
                "学生発表": student_presentation,
                "ひと言": message # 追加
            }
            
            try:
                with st.spinner("送信中です... しばらくお待ちください。"):
                    response = requests.post(GAS_URL, json=payload)
                
                if response.status_code == 200:
                    st.success("🎉 回答を受け付けました！")
                else:
                    st.error(f"⚠️ 送信に失敗しました（エラーコード: {response.status_code}）。再度お試しください。")
            except Exception as e:
                st.error(f"⚠️ エラーが発生しました: {e}")

    if st.button("管理者用ページへ移動する"):
        st.session_state["page"] = "admin"
        st.rerun()
