# Fix Mate 🛠️  
An AI-powered local assistant that helps you identify damages (like broken pipes) from an image and provides initial repair guidance.  
The project uses [Ollama](https://ollama.com) with a multimodal model to describe the image, and then processes the text for recommendations.

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/anonhossain/fix_mate.git
cd fix_mate
```
### 2️⃣ Create and Activate Virtual Environment
Create venv
``` bash

python -m venv .venv
```

# Activate venv
# On Windows (PowerShell)
.venv\Scripts\activate

### 3️⃣ Install Ollama

After installing, run:

```bash
ollama run gemma3:12b
```
