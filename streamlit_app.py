import streamlit as st
import requests
import base64

st.set_page_config(page_title="Trạm AI Kép Tự Trị", layout="centered")

st.title("🚀 Trạm Điều Khiển AI Kép Tự Trị")
st.caption("Phiên Bản Tinh Gọn Trên Đám Mây")

def push_to_github(token, repo, file_path, content, message="AI cập nhật code"):
    try:
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        user_res = requests.get("https://api.github.com/user", headers=headers).json()
        username = user_res.get("login")
        
        if not username:
            return "❌ Token không chính xác."

        url = f"https://api.github.com/repos/{username}/{repo}/contents/{file_path}"
        res = requests.get(url, headers=headers)
        sha = res.json().get("sha") if res.status_code == 200 else None
        
        content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        payload = {"message": message, "content": content_b64}
        if sha:
            payload["sha"] = sha
            
        put_res = requests.put(url, json=payload, headers=headers)
        if put_res.status_code in [200, 201]:
            return "✅ Đã lưu thành công!"
        else:
            return f"❌ Lỗi: {put_res.json().get('message')}"
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

with st.expander("⚙️ Cấu hình GitHub", expanded=False):
    txt_github_token = st.text_input("🔑 GitHub Token", type="password")
    txt_repo = st.text_input("📁 Tên Repository", value="tram-dieu-khien-ai")
    txt_file_path = st.text_input("📝 Đường dẫn file", value="app/src/main/java/MainActivity.kt")

st.markdown("---")

txt_input = st.text_area(
    "💬 Nêu yêu cầu hoặc mô tả lỗi cần sửa:",
    placeholder="Ví dụ: Tìm lỗi ở dòng 91 và sửa lại...",
    height=120
)

if st.button("🚀 BẮT ĐẦU XỬ LÝ", type="primary"):
    if not txt_input.strip():
        st.warning("💬 Anh chưa nhập yêu cầu nào cả!")
    else:
        with st.spinner("🔄 Hai Bộ Não đang làm việc..."):
            st.success("🧠 Bộ Não 1: Đã nhận yêu cầu, đang chuyển cho Bộ Não 2...")
            st.info(f"💻 Bộ Não 2: Đã phân tích:\n✅ Yêu cầu: {txt_input}\n✅ Sẵn sàng viết/sửa code")
            
            code_mau = """
// ==========================================
// Code mẫu từ Trạm AI Kép
// ==========================================
// Anh copy đoạn này và dán vào đúng vị trí nhé
class MainActivity : AppCompatActivity() {
    // Code sẽ xuất hiện ở đây
}
"""
            st.code(code_mau, language="kotlin")
            
            if txt_github_token:
                thong_bao = push_to_github(txt_github_token, txt_repo, txt_file_path, code_mau)
                st.markdown(f"📢 {thong_bao}")
            else:
                st.info("💡 Không có GitHub Token → chỉ hiển thị code thôi. Copy thủ công nhé!")
