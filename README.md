# 🚀  GPT_2 API Project

## 🪪 Thông tin sinh viên
- 24120278  
- Võ Văn Khánh Đăng  
- 24CTT3


## 📌 Giới thiệu   
- Tên Model : GPT2  
- [Link Model](https://huggingface.co/openai-community/gpt2)
---

## 📋 Mô tả chức năng 
- Hệ thống cung cấp API sinh văn bản tự động dựa trên mô hình GPT-2. Người dùng gửi vào một đoạn văn bản đầu vào (prompt), hệ thống sẽ xử lý và trả về nội dung được sinh tiếp theo một cách tự nhiên. API có thể được sử dụng cho các công việc như viết nội dung, hỗ trợ chatbot, hoặc tạo văn bản tự động.  

## ⚙️ Cài đặt thư viện

1. Mở termial  
2. Chạy dòng lệnh: 
```bash
pip install torch transformers fastapi uvicorn omegaconf requests
```

---

## ▶️ Chạy chương trình
1. Lưu file  
2. Mở terminal, chạy dòng lệnh:
```bash
uvicorn source:app --host 127.0.0.1 --port 8000 --reload ( hoặc py -m uvicorn source:app --host 127.0.0.1 --port 8000 --reload)
```
3. Sau khi chạy lệnh này, server sẽ bắt đầu lắng nghe tại địa chỉ http://127.0.0.1:8000, truy cập http://127.0.0.1:8000/docs để test API

---

## 🧪 Hướng dẫn gọi API
Base URL: http://127.0.0.1:8000 (Localhost)  
Swagger Docs: http://127.0.0.1:8000/docs  
Endpoint chính: Sinh văn bản (/predict)  
- Phương thức (Method): POST  
- Đường dẫn (URL): /predict  
- Headers: Content-Type: application/json  
- Body (JSON):  
    - prompt (chuỗi, bắt buộc): Đoạn văn bản đầu vào để model viết tiếp.  
    - max_length (số nguyên, tùy chọn, mặc định = 50): Độ dài tối đa của văn bản trả về (bao gồm cả prompt).  

1. Get/root
- Chức năng: Giới thiệu và mô tả chức năng của API
- Response mẫu :
```bash
{
  "message" : "GPT-2 Text Generation API",
  "description" : " API sinh văn bản sử dụng GPT-2",
  "endpoint" : [
    "/health"
    "/predict"
  ]
}
```

2. GET/ health
- Chức năng: kiểm tra trạng thái hoạt động của hệ thống.
- Response mẫu:
```bash
{
  "status" : "ok",
  "model" : "ready" 
} 
```

3. POST/predict
- Chức năng: nhận dữ liệu đầu vào từ người dùng, gọi mô hình
Hugging Face, và trả kết quả dưới dạng JSON.
- Response mẫu:
```bash
{
  "input": "string",
  "output": "string; câu trả lời của api",
  "status": "success"
}
```

---


## 📽️Video Demo
<video width="600" controls>
  <source src="Demo.mp4" type="video/mp4">
  Trình duyệt không hỗ trợ video.
</video>




