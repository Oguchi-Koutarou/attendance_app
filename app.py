import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

# --- パスワード認証 & 画面分岐機能 ---
def check_role():
    # セッション状態の初期化
    if "role" not in st.session_state:
        st.session_state["role"] = None

    # すでに認証済みの場合は現在の役割を返す
    if st.session_state["role"] in ["user", "admin"]:
        return st.session_state["role"]

    st.title("🔒 ログイン認証")
    st.write("参加者の方は「回答者用パスワード」を、管理者は「管理者用パスワード」を入力してください。")
    
    input_password = st.text_input("パスワードを入力", type="password")
    
    if st.button("ログイン"):
        # ★ ここでパスワードを自由に設定してください
        if input_password == "inverter":  # 回答者用のパスワード
            st.session_state["role"] = "user"
            st.rerun()
        elif input_password == "converter":  # 管理者用のパスワード
            st.session_state["role"] = "admin"
            st.rerun()
        else:
            st.error("⚠️ パスワードが間違っています。")
            
    return None

role = check_role()

# 認証されるまでここでストップ
if role is None:
    st.stop()

# ==========================================
# 【ロール1】管理者用画面
# ==========================================
if role == "admin":
    st.title("📊 管理者専用：出欠集計ダッシュボード")
    st.success("管理者としてログインしました。")
    
    file_name = "secret_attendance_results.csv"
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        st.write("### 回答一覧")
        st.dataframe(df)
        
        st.write("---")
        st.write("**【出欠サマリー】**")
        if "出欠" in df.columns:
            st.write(df["出欠"].value_counts())
            
        st.write("---")
        # Excelダウンロード機能
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='出欠回答一覧')
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 回答結果をExcelでダウンロード",
            data=excel_data,
            file_name="attendance_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("まだ回答データはありません。")
        
    if st.button("ログアウトする"):
        st.session_state["role"] = None
        st.rerun()

# ==========================================
# 【ロール2】回答者用画面
# ==========================================
elif role == "user":
    st.title("TMU Annual Research Forum")
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
            friday_party = st.radio("金曜夜の懇親会（4,500 円/人）への参加", ["参加", "不参加"])
            saturday_party = st.radio("土曜夜の懇親会（3,000 円/人）への参加", ["参加", "不参加"])
            
            st.markdown("---")
            st.subheader("5. 属性情報")
            occupation = st.selectbox("職業をお選びください *", ["学生", "教員", "企業", "その他"])
        
        #comment = st.text_area("一言メッセージ（任意）")
        
        submitted = st.form_submit_button("回答を送信する")
        
        if submitted:
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
                    "職業": occupation,
                    #"コメント": comment
                }])
                
                if os.path.exists(file_name):
                    new_data.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')
                else:
                    new_data.to_csv(file_name, index=False, encoding='utf-8-sig')
                    
                st.success(f"🎉 {name_kanji}さんの回答を受け付けました！ご協力ありがとうございます。")

    st.write("---")
    if st.button("ログアウトする"):
        st.session_state["role"] = None
        st.rerun()
