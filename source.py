# Cấu hình 
with open("config.yaml", "w") as f:
    f.write("""
model_path: openai-community/gpt2

student_info:
  name: "Vo Van Khanh Dang"
  id: "24120278"
""")

# Load Model
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from omegaconf import OmegaConf

class GPT2Generator:
    def __init__(self, config_path):
        self.cfg = OmegaConf.load(config_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.cfg.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(self.cfg.model_path)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def __call__(self, prompt, max_length=50):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                do_sample=True,
                top_k=50,
                top_p=0.95
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


# Test Model
generator = GPT2Generator("config.yaml")

test_text = "Hello, my name is"
result = generator(test_text)

print("Input:", test_text)
print("Output:", result)

# Tạo API
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import uvicorn

# ===== LOAD MODEL (1 lần) =====
try:
    generator = GPT2Generator("config.yaml")
except Exception as e:
    generator = None
    print("❌ Lỗi load model:", e)

# ===== APP =====
app = FastAPI(
    title="GPT-2 Text Generation API",
    description="Sinh văn bản với GPT-2",
    version="1.0"
)

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== REQUEST =====
class TextRequest(BaseModel):
    prompt: str
    max_length: int = 50

    class Config:
        schema_extra = {
            "example": {
                "prompt": "Once upon a time",
                "max_length": 50
            }
        }

@app.get("/")
def root():
    return {
        "message": "GPT-2 Text Generation API",
        "description": "API sinh văn bản sử dụng GPT-2",
        "endpoints": ["/health", "/predict"]
    }

@app.get("/health")
def health_check():
    if generator is None:
        return {"status": "error", "model": "not loaded"}
    return {"status": "ok", "model": "ready"}

# ===== ROUTES =====
@app.post("/predict")
async def generate_post(request: TextRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt không hợp lệ!")

    if generator is None:
        raise HTTPException(status_code=500, detail="Model chưa load")

    try:
        result = generator(request.prompt, request.max_length)
        return {
            "input": request.prompt,
            "output": result,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Chạy Sever
def run_server():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    server.run()


thread = threading.Thread(target=run_server, daemon=True)
thread.start()

print("✅ Server running at http://127.0.0.1:8000")
print("👉 Docs: http://127.0.0.1:8000/docs")

# Test API
import requests

url = "http://127.0.0.1:8000/predict"

# Test case 1
payload1 = {
    "prompt": "while dog sleeping ",
    "max_length": 50
}

# Test case 2
payload2 = {
    "prompt": "When a person dies",
    "max_length": 60
}

res1 = requests.post(url, json=payload1)
res2 = requests.post(url, json=payload2)

print("=== Test 1 ===")
print(res1.json())

print("\n=== Test 2 ===")
print(res2.json())
