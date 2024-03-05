"""
Pramithas Upreti
12/01/2022
CS152B
Final Project
mechanics.py

Single-Particle 1D Quantum Mechanics module.
It constitutes of two classes: WaveFunctionCreator and UnitaryOperation.
WaveFunctionCreator sets up and normalizes the wave. 
It uses Fourier transform to decompose our wave function into real and imaginary constituents.
UnitaryOperation helps us evolve time for our simulation and manipulates the potential.

This module is only a collection of classes, so there is no point in running it.
"""

#import statements
import numpy as np
from collection import constant


class WaveFunctionCreator(constant):
    """This is the Wavefunction class in 1D.
    The wave function is essentially represented in the form of Dirac Notation (Bra-Ket) through integration and complex conjugation using the NumPy library. """
    
    def __init__(self, waveform):
        super().__init__()
        if callable(waveform):
            try:
                self.x = waveform(np.linspace(self.x0,(self.L + self.x0),self.N))
            except:
                tmpx = np.linspace(self.x0, (self.L + self.x0), self.N)
                self.x = np.array([waveform(x) for x in tmpx])
            try:
                len(self.x)
            except TypeError as E:
                print(E)
        elif isinstance(waveform, np.ndarray):
            self.x = waveform


    def normalize(self):
        """Normalize the wavefunction through integration and complex conjugation"""
        try:
            #Sets up the equation, using Fourier transform
            self.x = self.x/np.sqrt(np.trapz(np.conj(self.x)*self.x, dx=self.dx))
        except FloatingPointError as E:
            print(E)


class UnitaryOperation(constant):
    """A unitary operator that dictates time evolution of the wavefunction.
    Unitary time evolution is the specific type of time evolution where probability is conserved. 
    In quantum mechanics, one typically deals with unitary time evolution. 
    Physically, it means that the probability of the existence of the quantum system does not change with time. 
    The quantum system exists at t=0 with probability=1, and also at t=T with probability=1."""

    def __init__(self, Potential):
        """Initialize the unitary operator."""
        super().__init__()
        if isinstance(Potential, np.ndarray):
            V = Potential
        elif callable(Potential):
            x = np.linspace(self.x0, (self.L + self.x0), self.N)
            V = np.array([Potential(xi) for xi in x])
        V *= self._scales
        # Get constant
        m, hbar, e, L, N, dx, dt = self._get_constant()
        # Initialize A and B matrices
        A = np.zeros([N, N], np.complex64)
        B = np.zeros([N, N], np.complex64)
        K = (dt*1.0j*hbar)/(4*m*dx**2)
        J = (dt*1.0j)/(2*hbar)
        # Initialize the constant, nonzero elements of the A and B matrices
        a1 = 1 + 2*K
        a2 = -K
        b1 = 1 - 2*K
        b2 = K
        # Construct the A and B matrices
        for i in range(N-1):
            A[i][i] = a1 + J*V[i]
            B[i][i] = b1 - J*V[i]
            A[i][i+1] = a2
            A[i+1][i] = a2
            B[i][i+1] = b2
            B[i+1][i] = b2
        A[N-1][N-1] = a1 + J*V[N-1]
        B[N-1][N-1] = b1 - J*V[N-1]
        # Obtain U
        self.U = np.dot(np.linalg.inv(A), B)
        # The identity operator is what the unitary matrix reduces to at time zero. 
        self.id = np.identity(len(self.U[0]), np.complex)


    def __call__(self, wavefunction):
        """Call this class on a wavefunction to time evolve it."""
        try:
            #returns the matrix multiplication of the two
            wavefunction.x = np.matmul(self.U, wavefunction.x)
        except FloatingPointError:
            pass