import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- パスワード認証機能 ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "inverter":  # ← ここに任意のパスワードを設定
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 ログイン認証")
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔒 ログイン認証")
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        st.error("⚠️ パスワードが間違っています。")
        return False
    else:
        return True

# パスワードが一致しない場合はここでストップ
if not check_password():
    st.stop()

# ==========================================
# ここから下がアンケート本編
# ==========================================
st.title("📅 イベント出欠・懇親会アンケート")
st.write("以下のフォームに必要事項を入力して送信してください。")

with st.form("attendance_form"):
    st.subheader("1. 基本情報")
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
        friday_party = st.radio("金曜夜の懇親会への参加", ["参加", "不参加"])
        saturday_party = st.radio("土曜夜の懇親会への参加", ["参加", "不参加"])
        
        st.markdown("---")
        st.subheader("5. 属性情報")
        occupation = st.selectbox("職業をお選びください *", ["学生", "教員", "企業", "その他"])
    
    comment = st.text_area("一言メッセージ（任意）")
    
    submitted = st.form_submit_button("回答を送信する")
    
    if submitted:
        if not name_kanji or not name_furigana:
            st.warning("⚠️ お名前（漢字とふりがな）は必須です。入力してください。")
        else:
            file_name = "secret_attendance_results.csv"  # 推測されにくいファイル名
            
            new_data = pd.DataFrame([{
                "日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "お名前（漢字）": name_kanji,
                "お名前（ふりがな）": name_furigana,
                "出欠": attendance_status,
                "参加日程": days_choice,
                "金曜懇親会": friday_party,
                "土曜懇親会": saturday_party,
                "職業": occupation,
                "コメント": comment
            }])
            
            if os.path.exists(file_name):
                new_data.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')
            else:
                new_data.to_csv(file_name, index=False, encoding='utf-8-sig')
                
            st.success(f"🎉 {name_kanji}さんの回答を受け付けました！ご協力ありがとうございます。")

# 管理者用：現在の集計結果
with st.expander("📊 管理者用：現在の集計結果を見る"):
    file_name = "secret_attendance_results.csv"
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        st.dataframe(df)
        
        st.write("---")
        st.write("**【出欠サマリー】**")
        if "出欠" in df.columns:
            st.write(df["出欠"].value_counts())
    else:
        st.info("まだ回答はありません。")