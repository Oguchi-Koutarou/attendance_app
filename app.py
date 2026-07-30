import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- パスワード認証機能 ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.title("🔒 ログイン認証")
    st.write("イベントの出欠アンケートです。パスワードを入力してください。")
    
    input_password = st.text_input("パスワードを入力", type="password")
    
    if st.button("ログイン"):
        if input_password == "inverter":  # 回答者用のパスワード
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("⚠️ パスワードが間違っています。")
            
    return False

if not check_password():
    st.stop()

# ==========================================
# アンケート回答画面（管理者画面なし）
# ==========================================
st.title("TMU Annual Research Forum")
st.write("以下のフォームに必要事項を入力して送信してください。")

with st.form("attendance_form"):
    st.subheader("1. 基本情報")
    name_kanji = st.text_input("お名前（漢字） *")
    name_furigana = st.text_input("お名前（ふりがな） *")
    
    st.subheader("2. 参加の是非")
    attendance_status = st.radio("イベントへの参加について", ["参加", "不参加"])
    
    # 初期値（不参加の場合のデフォルト値）
    days_choice = "ー"
    friday_party = "ー"
    saturday_party = "ー"
    occupation = "ー"
    
    # 「参加」を選んだ場合のみ、以降の質問項目を表示する
    if attendance_status == "参加":
        st.markdown("---")
        st.subheader("3. 参加日程について")
        days_choice = st.radio(
            "参加される日程をお選びください *", 
            ["両日参加", "金曜のみ参加", "土曜のみ参加"]
        )
        
        st.markdown("---")
        st.subheader("4. 懇親会への参加について")
        friday_party = st.radio("金曜夜の懇親会（4,500 円/人）への参加", ["参加", "不参加"])
        saturday_party = st.radio("土曜夜の懇親会（3,000 円/人）への参加", ["参加", "不参加"])
        
        st.markdown("---")
        st.subheader("5. 属性情報")
        occupation = st.selectbox("職業をお選びください *", ["学生", "教員", "企業", "その他"])
    
    submitted = st.form_submit_button("回答を送信する")
    
    if submitted:
        if not name_kanji or not name_furigana:
            st.warning("⚠️ お名前（漢字とふりがな）は必須です。入力してください。")
        else:
            file_name = "secret_attendance_results.csv"
            
            # 回答データの作成
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
            
            # クラウド（ローカルファイル）に自動追記・保存
            if os.path.exists(file_name):
                new_data.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(file_name, index=False, encoding='utf-8-sig')
                
            st.success(f"🎉 {name_kanji}さんの回答を受け付けました！ご協力ありがとうございます。")

st.write("---")
if st.button("ログアウトする"):
    st.session_state["authenticated"] = False
    st.rerun()
