





# Clap-to-Click



A hands-free media control tool that lets you **click anywhere using just sound**—whether it's a clap or your voice. Ideal for watching anime or videos without touching the computer!

---

##  Features

- **Clap detection**: Detects sharp claps and transforms them into a mouse click.
- **Voice detection**: Recognizes the words "play" or "pause" and clicks automatically.
- **Fast & Responsive**: Optimized for low latency with minimal lag.
- **Debouncing**: Prevents multiple clicks from a single sound—ensures one click per clap or voice command.
- **GUI Status**: A simple Tkinter window displays real-time status messages.

---

##  Demo

| Action        | Result                          |
|---------------|----------------------------------|
| Clap your hands |  Click wherever the cursor is |
| Say "play" or "pause" loudly |  Click triggers play/pause |

---

##  Getting Started

### Prerequisites

- Python 3.8 or higher
- A working microphone
- The Vosk English voice model folder `vosk-model-small-en-us-0.15` placed in the project directory (same folder as `clap.py`)

### Installation

```bash
git clone https://github.com/ICLIPTER/Clap-to-Click.git
cd Clap-to-Click
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
