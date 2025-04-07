# Quantum Particle Simulation in 1D Potential

This project is a simulation of a single quantum particle inside a bounded one-dimensional potential. It is a complex simulation that leverages multiple core computer science and quantum mechanics concepts.

## 🔧 Core Concepts

- **Code Reuse**: Modular design allows reusing existing code for new functions.
- **Modular Design**: The project is split into independent modules or classes.
- **Object-Oriented Programming**: Utilizes classes and inheritance to encapsulate behavior.
- **Python Libraries**: Uses `NumPy`, `SciPy`, `SymPy`, `Matplotlib`, and `Tkinter`.

## 📖 Project Description

This simulation app allows users to input a wave equation Ψ(x) and a potential V(x), which define the behavior of a quantum particle. Users can manipulate these values using the GUI.

### Default Values

- Wavefunction:  
  $$\Psi(x) = e^{-0.5(20(x - 0.25)^2)}$$
- Potential:  
  $$V(x) = 2x^2$$

### Quantum Mechanics Involved

The particle’s behavior is governed by:

> $$|\Psi(t)\rangle = U(t) |\Psi(0)\rangle$$

Where:
- $$|\Psi(0)\rangle$$ is the initial wavefunction vector,
- $$U(t)$$ is the unitary time evolution matrix.

Unitary evolution ensures conservation of probability over time.

### Key Features

- Draw wavefunctions and potentials with your mouse.
- Real-time updating of Ψ(x) and V(x).
- Toggle between wavefunction and probability density view.
- Animation and interactivity powered by `Tkinter`.
- Real-time reshaping of Ψ(x) and V(x) using mouse input.
- Boolean attributes track whether wave/potential reshaping occurred and pauses/resumes simulation appropriately.

## 💻 How to Run

Run the simulation by executing:

```bash
python main.py
```

You will see a GUI showing the wavefunction within the boundary -0.5 < x < 0.5. The GUI includes:
- Entry boxes for Ψ(x) and V(x),
- Mouse drawing options,
- A button to toggle probability distribution,
- A slider to control animation speed.

## 📊 Visualization

- **Blue and Orange Lines**: Represent the real and imaginary parts of Ψ(x).
- **Probability Density**: Shown via the square of the wavefunction’s magnitude.

## 🧩 Project Structure

- `main.py`: GUI interface and main driver class `Wave`, inherited from `Quantum`.
- `qmanimate.py`: Handles plotting using `Quantum`, a child class of `constant`.
- `mechanics.py`: Includes `WaveFunctionCreator` (for wave vectorization) and `UnitaryOperation` (for time evolution).
- `collection.py`: Contains utility classes like `constant` (sets natural units) and `Function` (parsing user-defined functions).
