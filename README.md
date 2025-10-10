# 🎮 Making Games Accessible for Blind Players

This research project, developed under Professor Yotam Gingold at George Mason University, explores how 2D and 3D games can be made accessible to blind players through AI-powered scene narration.

## 🚀 Overview
The system extracts frames from gameplay videos and converts them into descriptive narration using:
- **GPT-4 Vision** for frame understanding
- **DeepGram Aura** for real-time text-to-speech
- **Persistent memory** and **adaptive frame selection** for coherent narration

## 🧩 Features
- Real-time scene narration
- Interactive navigation loop (`next`, `back`, `repeat`, `quit`)
- Caching system to prevent redundant analysis
- Keyframe detection for optimal description generation

## ⚙️ Installation
\`\`\`bash
git clone https://github.com/Youssef-2060/MAKING_GAMES_ACCESSIBLE_FOR_BLIND_PEOPLE.git
cd MAKING_GAMES_ACCESSIBLE_FOR_BLIND_PEOPLE
pip install -r requirements.txt
python3 "OpenAI GPT-4 Vision and DeepGraum Aura Pipeline.py"
\`\`\`

