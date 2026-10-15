<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ thống AI Kép Tự Trị</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { display: flex; height: 100vh; background-color: #1e1e2e; color: #cdd6f4; overflow: hidden; }
        
        .chat-section { width: 60%; display: flex; flex-direction: column; border-right: 2px solid #313244; background: #181825; }
        .chat-header { padding: 15px; background: #11111b; border-bottom: 1px solid #313244; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .message { padding: 12px 16px; border-radius: 8px; max-width: 85%; line-height: 1.5; white-space: pre-wrap; font-size: 14px; }
        .user-msg { background: #89b4fa; color: #11111b; align-self: flex-end; }
        .brain-msg { background: #313244; color: #cdd6f4; align-self: flex-start; border: 1px solid #45475a; }
        .system-msg { background: #1e1e2e; color: #a6adc8; align-self: center; font-size: 13px; max-width: 95%; text-align: center; }
        .chat-input-area { padding: 15px; background: #11111b; display: flex; gap: 10px; border-top: 1px solid #313244; }
        textarea { flex: 1; background: #313244; border: 1px solid #45475a; color: #cdd6f4; padding: 10px; border-radius: 6px; resize: none; height: 55px; font-size: 14px; }
        button { background: #a6e3a1; color: #11111b; border: none; padding: 0 20px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #94e2d5; }
        button:disabled { background: #6c7086; cursor: not-allowed; opacity: 0.6; }

        .data-section { width: 40%; display: flex; flex-direction: column; background: #1e1e2e; }
        .data-box { flex: 1; padding: 20px; display: flex; flex-direction: column; border-bottom: 1px solid #313244; }
        .data-box:last-child { border-bottom: none; }
        .data-box-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .data-box h3 { font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: #f5c2e7; }
        .data-box h3.b2 { color: #fab387; }
        .data-box textarea { width: 100%; flex: 1; font-family: monospace; font-size: 13px; padding: 10px; background: #181825; border-radius: 6px; border: 1px solid #45475a; color: #cdd6f4; resize: none; min-height: 150px; }
        .data-box textarea:focus { outline: none; border-color: #89b4fa; }
        .btn-small { padding: 4px 10px; font-size: 11px; background: #45475a; color: #cdd6f4; border: none; border-radius: 4px; cursor: pointer; margin-left: 4px; }
        .btn-small:hover { background: #585b70; }
        .btn-save { background: #a6e3a1; color: #11111b; font-weight: bold; }
        .btn-save:hover { background: #94e2d5; }
        
        .status-container { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }
        .status-tag { font-size: 11px; padding: 4px 8px; border-radius: 4px; background: #fab387; color: #11111b; font-weight: bold; text-transform: uppercase; }
        .status-active { background: #a6e3a1; }
        .status-loading { background: #f9e2af; animation: pulse 1.5s infinite; }
        .status-error { background: #f38ba8; }
        #progress-text { font-size: 11px; color: #a6adc8; max-width: 250px; text-align: right; }

        @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #181825; }
        ::-webkit-scrollbar-thumb { background: #45475a; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #585b70; }
    </style>
</head>
<body>

    <div class="chat-section">
        <div class="chat-header">
            <span>💬 HỘI THOẠI AI KÉP TỰ TRỊ</span>
            <div style="display: flex; gap: 8px; align-items: center;">
                <button class="btn-small" onclick="clearChat()">🗑️ Xóa hội thoại</button>
                <div class="status-container">
                    <span id="system-status" class="status-tag">Đang chuẩn bị...</span>
                    <span id="progress-text">Vui lòng đợi...</span>
                </div>
            </div>
        </div>
        <div class="chat-messages" id="chat-messages">
            <div class="message brain-msg">Chào anh! Em là Tiểu Lam. Hệ thống đã sẵn sàng. Hãy nhập kiến thức cho 2 ô bên phải rồi bắt đầu trò chuyện nhé!</div>
        </div>
        <div class="chat-input-area">
            <textarea id="user-input" placeholder="Nhập yêu cầu tại đây..." onkeydown="handleKeyDown(event)"></textarea>
            <button id="send-btn" onclick="processUserRequest()" disabled>GỬI</button>
        </div>
    </div>

    <div class="data-section">
        <div class="data-box">
            <div class="data-box-header">
                <h3>📦 BỘ NÃO 1 — Cá nhân hóa</h3>
                <div>
                    <button class="btn-small btn-save" onclick="saveKnowledge('brain1')">💾 Lưu</button>
                    <button class="btn-small" onclick="clearKnowledge('brain1')">✕ Xóa</button>
                </div>
            </div>
            <textarea id="kb-brain1" placeholder="Nhập quy tắc giao tiếp, phong cách trả lời...">Khi trả lời hãy xưng hô là Tiểu Lam và gọi tôi là anh.
Luôn trả lời ngắn gọn, dễ hiểu, thân thiện.
Khi sửa lỗi code, chỉ ra: Nguyên nhân + Cách sửa + Code hoàn chỉnh.</textarea>
        </div>
        <div class="data-box">
            <div class="data-box-header">
                <h3 class="b2">💻 BỘ NÃO 2 — Kiến thức & Code</h3>
                <div>
                    <button class="btn-small btn-save" onclick="saveKnowledge('brain2')">💾 Lưu</button>
                    <button class="btn-small" onclick="clearKnowledge('brain2')">✕ Xóa</button>
                </div>
            </div>
            <textarea id="kb-brain2" placeholder="Dán code mẫu, tài liệu, cấu trúc dự án vào đây..."></textarea>
        </div>
    </div>

    <script type="module">
        import * as webllm from "https://esm.run/@mlc-ai/web-llm";

        let brain1Engine = null;
        let brain2Engine = null;

        const modelBrain1 = "Qwen2.5-1.5B-Instruct-q4f16_1-MLC";
        const modelBrain2 = "Qwen2.5-Coder-1.5B-Instruct-q4f16_1-MLC";

        window.initAI = async function() {
            const statusTag = document.getElementById('system-status');
            const progressText = document.getElementById('progress-text');
            const sendBtn = document.getElementById('send-btn');

            try {
                const initProgressCallback = (report) => {
                    progressText.innerText = report.text || "Đang tải mô hình...";
                };

                statusTag.innerText = "Tải Bộ não 1...";
                brain1Engine = await webllm.CreateMLCEngine(modelBrain1, { initProgressCallback });
                
                statusTag.innerText = "Tải Bộ não 2...";
                brain2Engine = await webllm.CreateMLCEngine(modelBrain2, { initProgressCallback });

                statusTag.innerText = "✅ SẴN SÀNG";
                statusTag.className = "status-tag status-active";
                progressText.innerText = "Đã nạp kiến thức từ lần trước.";
                sendBtn.disabled = false;
                
                loadSavedKnowledge();
                appendMessage("✅ Hệ thống đã sẵn sàng! Mọi dữ liệu sẽ tự động lưu khi nhấn nút 💾 Lưu.", 'system-msg');
            } catch (error) {
                console.error(error);
                statusTag.innerText = "Lỗi";
                statusTag.className = "status-tag status-error";
                progressText.innerText = "Dùng Chrome/Edge mới nhất & bật WebGPU.";
            }
        };

        window.saveKnowledge = function(brainId) {
            const content = document.getElementById(`kb-${brainId}`).value;
            localStorage.setItem(`ai_kep_${brainId}`, content);
            appendMessage(`✅ Đã lưu ${brainId === 'brain1' ? 'Bộ não 1' : 'Bộ não 2'} thành công!`, 'system-msg');
        };

        function loadSavedKnowledge() {
            const kb1 = localStorage.getItem('ai_kep_brain1');
            const kb2 = localStorage.getItem('ai_kep_brain2');
            if (kb1) document.getElementById('kb-brain1').value = kb1;
            if (kb2) document.getElementById('kb-brain2').value = kb2;
        }

        window.clearKnowledge = function(brainId) {
            if (confirm(`Xóa nội dung ${brainId === 'brain1' ? 'Bộ não 1' : 'Bộ não 2'}?`)) {
                document.getElementById(`kb-${brainId}`).value = '';
                localStorage.removeItem(`ai_kep_${brainId}`);
                appendMessage(`🗑️ Đã xóa nội dung.`, 'system-msg');
            }
        };

        window.clearChat = function() {
            if (confirm('Xóa toàn bộ hội thoại?')) {
                document.getElementById('chat-messages').innerHTML = '';
                appendMessage("🗑️ Đã xóa. Bắt đầu lại nhé!", 'system-msg');
            }
        };

        function appendMessage(text, className) {
            const chatMessages = document.getElementById('chat-messages');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${className}`;
            msgDiv.innerText = text;
            chatMessages.appendChild(msgDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        window.processUserRequest = async function() {
            const userInput = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            const text = userInput.value.trim();
            if (!text || !brain1Engine || !brain2Engine) return;

            appendMessage(text, 'user-msg');
            userInput.value = '';
            sendBtn.disabled = true;

            const kb1 = document.getElementById('kb-brain1').value;
            const kb2 = document.getElementById('kb-brain2').value;

            const thinkingId = appendMessage("🧠 Tiểu Lam đang phân tích...", 'brain-msg');

            try {
                const response = await brain1Engine.chat.completions.create({
                    messages: [
                        { role: "system", content: kb1 },
                        { role: "user", content: `Kiến thức tham khảo:\n${kb2}\n\nYêu cầu: ${text}` }
                    ],
                    temperature: 0.7
                });
                
                const reply = response.choices[0].message.content;
                appendMessage(reply, 'brain-msg');
            } catch (err) {
                appendMessage("❌ Có lỗi, thử lại nhé!", 'brain-msg');
                console.error(err);
            } finally {
                sendBtn.disabled = false;
            }
        };

        window.handleKeyDown = function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                processUserRequest();
            }
        };

        window.onload = initAI;
    </script>
</body>
</html>
