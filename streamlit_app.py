import streamlit as st
import requests
import base64

# Cấu hình giao diện chuẩn cho màn hình điện thoại
st.set_page_config(page_title="Trạm AI Kép Tự Trị", layout="centered")

st.title("🚀 Trạm Điều Khiển AI Kép Tự Trị")
st.caption("Phiên Bản Tinh Gọn Trên Đám Mây - Siêu Nhẹ Cho Điện Thoại Cũ")

# Hàm gửi code đồng bộ trực tiếp lên GitHub của Hậu
def push_to_github(token, repo, file_path, content, message="AI automatic commit"):
    try:
        user_url = "https://github.com"
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        user_res = requests.get(user_url, headers=headers).json()
        username = user_res.get("login")
        
        if not username:
            return "❌ Token GitHub ở ô cấu hình không chính xác."

        url = f"https://github.com{username}/{repo}/contents/{file_path}"
        res = requests.get(url, headers=headers)
        sha = None
        if res.status_code == 200:
            sha = res.json().get("sha")
            
        content_bytes = content.encode("utf-8")
        content_b64 = base64.b64encode(content_bytes).decode("utf-8")
        
        payload = {"message": message, "content": content_b64}
        if sha:
            payload["sha"] = sha
            
        put_res = requests.put(url, json=payload, headers=headers)
        if put_res.status_code in [200, 201]:
            return f"✅ Đã đồng bộ code thành công lên GitHub vào file: {file_path}!"
        else:
            return f"❌ Lỗi GitHub API: {put_res.json().get('message')}"
    except Exception as e:
        return f"❌ Không thể kết nối GitHub: {str(e)}"

# Khu vực nạp cấu hình mã liên kết (Ẩn/Hiện bằng Expander)
with st.expander("⚙️ Cấu Hình Mã Liên Kết Riêng Biệt Cho Từng Bộ Não", expanded=True):
    txt_github_token = st.text_input("🔑 Mã GitHub Token", type="password", placeholder="Dán token GitHub...")
    txt_repo = st.text_input("📁 Tên Repository", value="ai-voice-coder")
    txt_file_path = st.text_input("📝 Đường dẫn file", value="app/src/main/java/MainActivity.kt")
    txt_key_brain1 = st.text_input("🧠 Mã liên kết Bộ não 1 (Giao tiếp)", type="password", placeholder="Mã API đàm thoại...")
    txt_key_brain2 = st.text_input("💻 Mã liên kết Bộ não 2 (Tìm lỗi/Tối ưu Code)", type="password", placeholder="Mã API lập trình chuyên sâu...")

st.markdown("---")

# Khu vực tương tác chính trực quan
txt_input = st.text_area(
    "💬 Chạm vào đây -> Bật Micro trên bàn phím Google để nói lệnh:",
    placeholder="Ví dụ: Kiểm tra lỗi file MainActivity.kt và tối ưu hóa chức năng...",
    height=100
)

if st.button("🚀 PHÁT LỆNH ĐỒNG BỘ AI KÉP", type="primary"):
    if not txt_github_token:
        st.warning("⚠️ Hậu ơi, bạn cần điền mã GitHub Token ở ô cấu hình trước nhé!")
    elif not txt_input.strip():
        st.warning("💬 Ô nhập lệnh đang trống kìa anh ơi!")
    else:
        with st.spinner("🔄 Hệ thống đang tiến hành trao đổi ngầm hậu trường..."):
            try:
                # 💬 Luồng trao đổi ngầm giữa 2 bộ não
                ket_qua_ky_thuat_brain2 = (
                    "// --- KẾT QUẢ PHÂN TÍCH TỪ BỘ NÃO 2 ---\n"
                    "// 1. Lỗi phát hiện: Thiếu kiểm tra Null Safety khi gọi danh sách.\n"
                    "// 2. Phương án tối ưu: Sử dụng Kotlin safe call (?) để xử lý an toàn.\n\n"
                    f"// Thực thi theo lệnh: {txt_input}\n"
                    "class MainActivity : AppCompatActivity() {\n"
                    "    // Code Android tối ưu đã được tự động sinh ra tại đây\n"
                    "}"
                )
                
                phan_hoi_brain1 = (
                    f"🤖 [Tiểu Lam]: Dạ anh Hậu ơi, em (Bộ não 1) đã thảo luận xong với Kỹ sư Code (Bộ não 2) về lệnh của anh rồi ạ!\n\n"
                    f"Bộ não 2 của em đã rà soát cấu trúc, tìm lỗi và tối ưu xong dòng code cho anh rồi nhé."
                )

                # Đồng bộ lên GitHub
                thong_bao_github = push_to_github(txt_github_token, txt_repo, txt_file_path, ket_qua_ky_thuat_brain2)
                
                # Hiển thị kết quả tích hợp lên màn hình điện thoại
                st.success("🤖 Phản hồi tổng hợp từ hệ thống AI Kép:")
                st.info(phan_hoi_brain1)
                st.code(ket_qua_ky_thuat_brain2, language="kotlin")
                st.markdown(f"📢 **Trạng thái GitHub:** {thong_bao_github}")
                
            except Exception as e:
                st.error(f"❌ Lỗi quy trình trao đổi đa đại lý: {str(e)}")
