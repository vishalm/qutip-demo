# QuTiP Demo Setup Guide

## 📁 Project Structure Overview

```
qutip-demo/
├── demos/          # 🎪 Core quantum physics demonstrations
├── utils/          # 🛠️ Helper tools and utilities
├── docs/           # 📚 Documentation and guides
├── resources/      # 🖼️ Visual assets and screenshots
├── README.md       # 📋 Main project documentation
├── LICENSE         # 📄 MIT License
└── requirements.txt # 📦 Python dependencies
```

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/vishalm/qutip-demo.git
   cd qutip-demo
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python utils/verify_installation.py
   ```

4. **Run demos**
   ```bash
   # Interactive menu
   python utils/run_demos.py
   
   # Individual demos
   python demos/bloch_rabi_demo.py
   python demos/decoherence_demo.py
   python demos/cavity_qed_demo.py
   python demos/interactive_demo.py
   ```

## 📂 Directory Details

### `demos/` - Core Demonstrations
- **bloch_rabi_demo.py** - Bloch sphere visualization and Rabi oscillations
- **decoherence_demo.py** - Quantum decoherence and open system dynamics
- **cavity_qed_demo.py** - Cavity QED and quantum optics demonstrations
- **interactive_demo.py** - Real-time interactive controls and visualizations

### `utils/` - Utilities and Tools
- **run_demos.py** - Main demo launcher with interactive menu
- **verify_installation.py** - Installation verification and dependency checking
- **generate_screenshots.py** - Helper for generating documentation screenshots

### `docs/` - Documentation
- **CONTRIBUTING.md** - Contribution guidelines and development setup
- **SETUP.md** - This setup guide

### `resources/` - Visual Assets
- **screenshots/** - Demo output images for documentation
- Future: Could include additional resources like datasets, precomputed results

## 🔧 Development Setup

### For Contributors

1. **Fork and clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/qutip-demo.git
   cd qutip-demo
   ```

2. **Development environment**
   ```bash
   python3 -m venv dev-env
   source dev-env/bin/activate
   pip install -r requirements.txt
   ```

3. **Test changes**
   ```bash
   python utils/verify_installation.py
   python utils/run_demos.py
   ```

4. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### File Organization Rules

- **Keep demos/ clean** - Only core demonstration scripts
- **Use utils/ for helpers** - Installation, verification, screenshot tools
- **Document in docs/** - All documentation beyond main README
- **Visual assets in resources/** - Screenshots, diagrams, datasets

## 🎯 Best Practices

### Adding New Demos
1. Place new demo scripts in `demos/`
2. Update `utils/run_demos.py` menu
3. Add to `utils/verify_installation.py` file checks
4. Update README.md with description
5. Generate screenshots for documentation

### Code Organization
- Each demo script should be self-contained
- Use clear function names and docstrings
- Follow PEP 8 style guidelines
- Include educational comments explaining physics concepts

### Documentation
- Keep README.md as the main entry point
- Use docs/ for detailed guides
- Include screenshots in resources/screenshots/
- Update CONTRIBUTING.md for development guidelines

## 🐛 Troubleshooting

### Common Issues

1. **Import errors after reorganization**
   ```bash
   # Make sure you're running scripts from project root
   cd qutip-demo
   python utils/run_demos.py  # Correct
   cd utils && python run_demos.py  # May cause import issues
   ```

2. **Missing dependencies**
   ```bash
   python utils/verify_installation.py  # Check what's missing
   pip install -r requirements.txt     # Install all dependencies
   ```

3. **Path issues**
   - Always run commands from the project root directory
   - Use the full path when calling scripts (e.g., `python utils/run_demos.py`)

### Getting Help
- Check [README.md](../README.md) for detailed information
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bugs or questions

---

*This setup guide ensures you can quickly understand and work with the organized project structure.*
