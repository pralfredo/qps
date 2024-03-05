"""
Pramithas Upreti
12/01/2022
CS152B
Final Project
qmanimate.py

Matplotlib animation for graphing the single quantum particle wavefunction. 
This module is used in main.py for the graphing of the particle.
It contains the class Quantum, which is essentially where all the plots are created from the parsed input.

This module is only a collection of classes, so there is no point in running it.
"""

#import statements
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collection import Function, constant, scales
from mechanics import WaveFunctionCreator, UnitaryOperation
from time import perf_counter


class Quantum(constant):
    """Quantum class is essentially where all the lines are graphed after parsing the input. T
    his class is also a child class of the "constant" class of the “collection” module. 
    It uses the “Function” class of the “collection” module to manipulate and parse the functions.  
    Moreover, it also uses the “WaveFunctionCreator” class and the “UnitaryOperation” class of the “mechanics” module for carrying out the quantum manipulations. """

    def __init__(self, function="np.exp(-0.5*((x-0.25)/0.05)**2)", potential="(x)**2/2"):
        """Initialize the animation."""
        super().__init__()
        self._msg = ""  # Temporary messages in the text
        self._main_msg = ""  # Primary messages in this same text box.
        self._main_msg_store = "" # Store the primary message
        self.psi_name = ""  # Name of the wavefunction
        self.psi_latex = ""  # LaTEX name of the wavefunction
        self.V_name = ""   # Name of the potential
        self.V_latex = ""  # LaTEX name of the potential
        self.identity_matrix = np.identity(self.N, np.complex128)
        # Ticking int attributes
        self.fpi = 1    # Set the number of time evolutions per animation frame
        self._t = 0     # Time that has passed
        self._msg_i = 0  # Message counter for displaying temporary messages
        self.fps = 30    # frames per second
        self.fps_total = 0  # Total number of fps
        self.avg_fps = 0  # Average fps
        self.ticks = 0    # total number of ticks
        self._x_ticks = []
        self.t_perf = [1.0, 0.]
        self._dpi = 120
        # Boolean Attributes
        # Display the probability function or not
        self._display_probs = False
        self._scales_y = 1.0
        # Whether to show momentum p or to show position x
        self._show_p = False
        # Whether to show expectation value or not
        self._show_exp_val = False
        # tuple containing the position of the message
        self._msg_pos = (0, 0)
        # Numpy array of positions
        self.x = np.linspace(self.x0,(self.L + self.x0),self.N)
        # the parameters
        self.psi_base = None
        self.psi_params = {}
        self.V_base = None
        self.V_params = {}
        Function.add_function("arg", lambda theta: np.exp(2.0j*np.pi*theta))
        self.set_wavefunction(function)
        self.V_x = None
        self.set_unitary(potential)
        self._init_plots()


    def set_wavefunction(self, psi, normalize=True):
        """Parse input to set the wavefunction attributes."""
        if isinstance(psi, str):
            try:
                if psi.strip().replace(".", "").replace("-", "").replace("e", "").isnumeric():
                    psi_x = float(psi)*np.ones([self.N])
                    self.psi_name = psi
                    self.psi_latex = "$%s$" % psi
                    self.psi = WaveFunctionCreator(psi_x)
                    self._msg = "$\psi(x, 0) =$ %s" % self.psi_latex
                    self._msg_i = 45
                    if normalize:
                        self.psi.normalize()
                    self.psi_base = None
                    self.psi_params = {}
                else:
                    psi = psi.replace("^", "**")
                    f = Function(psi, "x")
                    self.psi_base = f
                    psi_func = lambda x: f(x, *f.get_tupled_default_values())
                    self.psi_name = str(f)
                    self.psi_latex = "$" + f.latex_repr + "$"
                    self.psi = WaveFunctionCreator(psi_func)
                    self.psi_params = f.get_enumerated_default_values()
                    self._msg = r"$\psi(x, 0) =$ %s" % self.psi_latex
                    self._msg_i = 45
                    if normalize:
                        self.psi.normalize()
            except (TypeError, AttributeError,SyntaxError, ValueError, NameError) as E:
                print(E)
        elif isinstance(psi, np.ndarray):
            self.psi = WaveFunctionCreator(psi)
            self.psi_name = "wavefunction"
            self.psi_latex = "$\psi(x)$"
            if normalize:
                self.psi.normalize()
        else:
            print("Unable to parse input")


    def set_unitary(self, V):
        """Parse input and set the unitary operator attributes.
        This also sets up the potential function attributes in the process."""
        if isinstance(V, str):
            try:
                if V.strip().replace(".", "").replace("-", "").replace("e", "").isnumeric():
                    self.V_name = ""
                    self.V_latex = str(np.round(float(V), 2))
                    if float(V) == 0:
                        V = 1e-30
                        V_f = float(V)*np.ones([self.N])
                        self.U_t = UnitaryOperation(np.copy(V_f))
                        self.V_x = 0.0*V_f
                    else:
                        V_f = scales(float(V)*np.ones([self.N]), 15)
                        self.V_x = V_f
                        self.U_t = UnitaryOperation(np.copy(V_f))
                        self.V_latex = "%sk" % (self.V_latex) if V_f[0] > 0 else " %sk" % (self.V_latex)
                    self.V_params = {}
                    self.V_base = None
                else:
                    V = V.replace("^", "**")
                    f = Function(V, "x")
                    self.V = lambda x: f(x, *f.get_tupled_default_values())
                    self.V_x = scales(self.V(self.x), 15)
                    self.V_name = str(f)
                    self.V_latex = "$" + f.multiply_latex_string("k") + "$"
                    self.U_t = UnitaryOperation(self.V)
                    self.V_base = f
                    self.V_params = f.get_enumerated_default_values()
            except (TypeError, AttributeError,SyntaxError, ValueError, NameError) as E:
                print(E)
        elif isinstance(V, np.ndarray):
            self.V_params = {}
            self.V_base = None
            self.V = None
            self.V_x = scales(V, 15)
            self.V_name = "V(x)"
            self.V_latex = "$V(x)$"
            self.U_t = UnitaryOperation(V)
        else:
            print("Unable to parse input")

        if hasattr(self, "lines"):
            self.updates_draw_potential()


    def updates_draw_potential(self):
        """updates the plot of the potential V(x)"""
        if np.amax(self.V_x > 0):
            V_max = np.amax(self.V_x[1:-2])
            self.lines[4].set_ydata(self.V_x/V_max*self.bounds[-1]*0.95)
            V_max *= self._scales
        elif np.amax(self.V_x < 0):
            V_max = np.abs(np.amin(self.V_x[1:-2]))
            self.lines[4].set_ydata(self.V_x/
                                    V_max*self.bounds[-1]*0.95)
            V_max *= self._scales
        else:
            V_max = self.bounds[-1]*0.95*self._scales
            self.lines[4].set_ydata(self.x*0.0)


    def display_probability(self, *args):
            """Show only the probability density"""
            self._display_probs = True
            self.lines[1].set_linewidth(1.25)
            self.lines[2].set_alpha(0.)
            self.lines[3].set_alpha(0.)
            if self._show_p:
                self.lines[0].set_text("—— $|\psi(p)|^2$")
            else:
                self.lines[0].set_text("—— $|\psi(x)|^2$")
            self.lines[6].set_alpha(0.)
            self.lines[7].set_alpha(0.)


    def display_wavefunction(self):
        """Show the wavefunction \psi(x) and hide the probability density."""
        self._display_probs = False
        self.lines[1].set_linewidth(0.75)
        self.lines[2].set_alpha(1.)
        self.lines[3].set_alpha(1.)
        self.lines[6].set_alpha(1.)
        self.lines[7].set_alpha(1.)
  

    def set_m(self, m, *args):
        """Change the mass of the particle"""
        self.m = m
        self.psi.m = m
        self.U_t.m = m
        self.set_unitary(self.V_x)


    def _change_constant(self, hbar):
        """Change constant"""
        self.hbar = hbar
        self.psi.hbar = hbar
        self.U_t.hbar = hbar
        self.set_unitary(self.V_x)


    def set_scales_y(self):
        """Set the scales y value.
        The scales y value determines how potential values shown on the plot is scalesd to its actual values."""
        if not self.potential_is_reshaped:
            if np.amax(self.V_x > 0):
                self._scales_y = np.amax(self.V_x[1:-2])/(
                    self.bounds[-1]*0.95)
            elif np.amax(self.V_x < 0):
                self._scales_y = np.abs(np.amin(self.V_x[1:-2]))/(
                    self.bounds[-1]*0.95)
            else:
                self._scales_y = 1.0
        else:
            self._scales_y = self.scales_y


    def _init_plots(self):
        """Start the animation, in which the required matplotlib objects are initialized and the plot boundaries are determined."""
        # Make matplotlib figure object
        self.figure = plt.figure(dpi=self._dpi)
        # Make a subplot object
        self.ax = self.figure.add_subplot(1, 1, 1)
        # Set the x limits of the plot
        xmin = self.x[0]
        xmax = self.x[-1]
        xrange = xmax - xmin
        self.ax.set_xlim(self.x[0] - 0.02*xrange, self.x[-1] + 0.02*xrange)
        self.ax.set_xlabel("x")
        # Set the y limits of the plot
        ymax = np.amax(np.abs(self.psi.x))
        ymin = -ymax
        yrange = ymax - ymin
        self.ax.get_yaxis().set_visible(False)
        self.ax.set_ylim(ymin-0.1*yrange, ymax+0.1*yrange)
        #all required lines for the plot
        line2, = self.ax.plot(self.x, np.real(self.psi.x),"-", animated=True, linewidth=0.5)
        line3, = self.ax.plot(self.x, np.imag(self.psi.x),"-", animated=True, linewidth=0.5)
        line1, = self.ax.plot(self.x, np.abs(self.psi.x), animated=True, color="black", linewidth=0.75)
        if np.amax(self.V_x > 0):
            line4, = self.ax.plot(self.x,(self.V_x/np.amax(self.V_x[1:-2]))*ymax*0.95,color="darkslategray",linestyle='-',linewidth=0.5)
        elif np.amax(self.V_x < 0):
            line4, = self.ax.plot(self.x,(self.V_x/np.abs(np.amin(self.V_x[1:-2]))*0.95*self.bounds[-1]),color="darkslategray",linestyle='-',linewidth=0.5)
        else:
            line4, = self.ax.plot(self.x,self.x*0.0,color="darkslategray",linestyle='-',linewidth=0.5)
        line0 = self.ax.text((xmax-xmin)*0.01 + xmin,ymin + (ymax-ymin)*0.05,"—— $|\psi(x)|$",alpha=1.,animated=True,color="black")
        line5 = self.ax.text((xmax-xmin)*0.01 + xmin,ymin + (ymax-ymin)*0.,"—— $Re(\psi(x))$",alpha=1.,animated=True,color="C0")
        line6 = self.ax.text((xmax-xmin)*0.01 + xmin,ymin + (ymax-ymin)*(-0.05),"—— $Im(\psi(x))$",alpha=1.,animated=True,color="C1")
        line7 = self.ax.text((xmax-xmin)*0.01 + xmin,ymin + (ymax-ymin)*(0.1),"—— V(x)",alpha=1.,color="darkslategray")
        # Show the infinite square well boundary
        self.ax.plot([self.x0, self.x0], [-10, 10],
                     color="gray", linewidth=0.75)
        self.ax.plot([self.x0+self.L, self.x0+self.L], [-10, 10],
                     color="gray", linewidth=0.75)
        # Record the plot boundaries
        ymin, ymax = self.ax.get_ylim()
        xmin, xmax = self.ax.get_xlim()
        self.bounds = xmin, xmax, ymin, ymax
        # Store each line in a list.
        self.lines = [line0, line1, line2, line3,line4,line5, line6,line7]
        # Another round of setting up and scaling the line plots
        if np.amax(self.V_x > 0):
            V_max = np.amax(self.V_x[1:-2])
            V_scales = self.V_x/V_max*self.bounds[-1]*0.95
            V_max *= self._scales
            self.lines[4].set_ydata(V_scales)
        elif np.amax(self.V_x < 0):
            V_max = np.abs(np.amin(self.V_x[1:-2]))
            V_scales = self.V_x/V_max*self.bounds[-1]*0.95
            V_max *= self._scales
            self.lines[4].set_ydata(V_scales)
        else:
            self.lines[4].set_ydata(self.x*0.0)
        # Manually plot gird lines
        maxp = self.bounds[-1]*0.95
        self.ax.plot([self.x0, self.x0+self.L], [0., 0.],color="gray", linewidth=0.5, linestyle="--")
        self.ax.plot([self.x0, self.x0+self.L], [maxp, maxp],color="gray", linewidth=0.5, linestyle="--")
        self.ax.plot([self.x0, self.x0+self.L], [-maxp, -maxp],color="gray", linewidth=0.5, linestyle="--")


    def _animate(self, i: int) -> list:
        """Produce a single frame of animation.
        This of course involves advancing the wavefunctionin time using the unitary operator."""
        self.t_perf[0] = self.t_perf[1]
        self.t_perf[1] = perf_counter()
        # Time evolve the wavefunction
        for _ in range(self.fpi):
            self.U_t(self.psi)
            self._t += self.dt
        # Define and set psi depending on whether to show psi in the positionor momentum basis.
        if self._show_p:
            psi = self.psi.p
        else:
            psi = self.psi.x
        # Set probability density or absolute value of wavefunction
        if self._display_probs:
            try:
                self.lines[1].set_ydata(
                    np.real(np.conj(psi)*psi)/3.0)
            except FloatingPointError as E:
                print(E)
        else:
            self.lines[1].set_ydata(np.abs(psi))
        # Set real and imaginary values
        self.lines[2].set_ydata(np.real(psi))
        self.lines[3].set_ydata(np.imag(psi))
        # Find fps stats
        t0, tf = self.t_perf
        self.ticks += 1
        self.fps = int(1/(tf - t0 + 1e-30))
        if self.ticks > 1:
            self.fps_total += self.fps
        self.avg_fps = int(self.fps_total/(self.ticks))
        if self.ticks % 60 == 0:
            pass
        return self.lines


    def animation_loop(self) -> None:
        """Produce all frames of animation."""
        self.main_animation = animation.FuncAnimation(self.figure, self._animate, blit=True,interval=1)