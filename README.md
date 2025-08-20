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

Activate venv On Windows (PowerShell)

``` bash
.venv\Scripts\activate
```

### 3️⃣ Install Ollama

After installing, run:

```bash
ollama run gemma3:12b
```

This will download the model locally.

4️⃣ Install Python Requirements

```bash

pip install -r requirements.txt
```

5️⃣ Run the Script

```bash
python img_to_text.py

```

### 📂 Project Structure

```bash

fix_mate/
│
├── file/
│   └── test.jpg           # Sample image
├── img_to_text.py         # Main script to process image
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

### 📝 How It Works

- User uploads image of a damaged object (e.g., broken pipe).
- Ollama multimodal model (like llava or gemma3 if vision-enabled) describes the image.
- The description is processed by a local language model to provide repair suggestions.

### ⚙️ Requirements
- Python 3.9+
- Ollama installed locally
- GPU recommended for faster inference
