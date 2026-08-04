import streamlit as st
import pandas as pd
from datetime import datetime
import os

# セッション状態の初期化
if "page" not in st.session_state:
    st.session_state["page"] = "user"  # 初期画面は「回答者用ページ」
if "admin_auth" not in st.session_state:
    st.session_state["admin_auth"] = False

# ==========================================
# 1. 管理者用ページ
# ==========================================
if st.session_state["page"] == "admin":
    st.title("🔒 管理者ログイン")
    
    # まだパスワード認証していない場合
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
            
    # パスワード認証成功後の管理者ページ本編
    else:
        st.title("📊 管理者専用ページ")
        st.success("管理者としてログインしました。")
        
        st.write("### 回答データのダウンロード")
        file_name = "secret_attendance_results.csv"
        if os.path.exists(file_name):
            with open(file_name, "rb") as f:
                st.download_button(
                    label="📥 最新の回答データをダウンロードする (CSV)",
                    data=f,
                    file_name="attendance_results.csv",
                    mime="text/csv"
                )
        else:
            st.info("まだ回答データはありません。")
            
        st.write("---")
        if st.button("ログアウトして回答ページに戻る"):
            st.session_state["admin_auth"] = False
            st.session_state["page"] = "user"
            st.rerun()

# ==========================================
# 2. 回答者用ページ（デフォルト）
# ==========================================
elif st.session_state["page"] == "user":
    st.title("TMU Annual Research Forum")
    st.write("以下のフォームに必要事項を入力して送信してください。")

    name_kanji = st.text_input("お名前（漢字） *")
    name_furigana = st.text_input("お名前（ふりがな） *")

    st.subheader("2. 参加の是非")
    attendance_status = st.radio("イベントへの参加について", ["参加", "不参加"])

    days_choice = "ー"
    friday_party = "ー"
    saturday_party = "ー"
    occupation = "ー"

    if attendance_status == "参加":
        st.markdown("---")
        st.subheader("3. 参加日程について")
        days_choice = st.radio(
            "参加される日程をお選びください *", 
            ["両日参加", "金曜のみ参加", "土曜のみ参加"]
        )
        
        st.markdown("---")
        st.subheader("4. 懇親会への参加について")
        friday_party = st.radio("金曜夜の懇親会（5,000 円/人 予定）への参加", ["参加", "不参加"])
        saturday_party = st.radio("土曜夜の懇親会（大人5,000 円/人，学生3,000 円/人 予定）への参加", ["参加", "不参加"])
        
        st.markdown("---")
        st.subheader("5. 属性情報")
        occupation = st.selectbox("職業をお選びください *", ["学生", "教員", "企業", "その他"])

    st.markdown("---")
    if st.button("回答を送信する", type="primary"):
        if not name_kanji or not name_furigana:
            st.warning("⚠️ お名前（漢字とふりがな）は必須です。入力してください。")
        else:
            file_name = "secret_attendance_results.csv"
            
            new_data = pd.DataFrame([{
                "日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "お名前（漢字）": name_kanji,
                "お名前（ふりがな）": name_furigana,
                "出欠": attendance_status,
                "参加日程": days_choice,
                "金曜懇親会": friday_party,
                "土曜懇親会": saturday_party,
                "職業": occupation
            }])
            
            if os.path.exists(file_name):
                new_data.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(file_name, index=False, encoding='utf-8-sig')
                
            st.success(f"🎉 {name_kanji}さんの回答を受け付けました！ご協力ありがとうございます。")

    # 画面の最下部にひっそりと「管理者用ページへ移動する」ボタンを配置
    st.write("---")
    if st.button("管理者用ページへ移動する"):
        st.session_state["page"] = "admin"
        st.rerun()
