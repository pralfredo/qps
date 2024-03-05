"""
Pramithas Upreti
12/01/2022
CS152B
Final Project
main.py

This module is the GUI simulation using Tkinter for viewing and interacting with the quantum simulation.
It displays the wave function along with the decomposed real and imaginary parts.
The user could insert a new wave function and potential to change the simulation.
It could be done through mouse clicks/drags or keyboard input of exact equations.
It also allows the user to show probability density of the particle's position along our 1D bound.

Run this file by typing py main.py for windows or python3.py for mac on the terminal.
"""

#import statements
import numpy as np
from mechanics import UnitaryOperation
from collection import constant, scales, change_array
from matplotlib.backends import backend_tkagg
from qmanimate import Quantum
import tkinter as tk


class wave(Quantum):
    """This class is the interactive Quantum Mechanics GUI object using Tkinter and Matplotlib.
    The “wave” class is run at the end of the file and is a GUI representation of a quantum particle bounded within a one-dimensional constraint. 
    It is a child class that inherits properties from the “Quantum” class of the “qmanimate” module. 
    Moreover, it uses the “WaveFunctionCreator” class and the “UnitaryOperation” class of the “mechanics” module for carrying out the quantum manipulations. """

    def __init__(self):
        """This is the Initializer for our wave function"""
        self.window = tk.Tk()
        #closes our simulation window on the press of the window manager's close button
        self.window.protocol('WM_DELETE_WINDOW', quit)
        self.window.title("Quantum Simulation")
        colour = self.window.cget('bg')
        if colour == 'SystemButtonFace': colour = "#F0F0F0"
        C = constant()
        x = np.linspace(C.x0, C.L + C.x0, C.N)
        # Default values for potential and wave function
        V = "(x)**2/2"
        psi = np.exp(-0.5*((x-0.25)/0.05)**2)
        # Initialize the inherited animation object
        Quantum.__init__(self, function=psi, potential=V)
        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.figure,master=self.window)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=20, columnspan=2)
        self.canvas.get_tk_widget().bind("<B1-Motion>",self.sketch)
        self.canvas.get_tk_widget().bind("<ButtonRelease-1>",self.sketch)
        try:
            self.figure.patch.set_facecolor(colour)
        except ValueError:
            pass
        # Mouse menu dropdown
        self.mouse_menu_label = tk.Label(self.window,text="Mouse:")
        self.mouse_menu_label.grid(row=7,column=3,sticky=tk.W + tk.E + tk.S,padx=(10, 10),columnspan=2)
        # Mouse menu tuple
        self.mouse_menu_tuple = ("Reshape Wavefunction","Reshape Wavefunction in Real Time","Reshape Potential V(x)")
        # Mouse menu string
        self.mouse_menu_string = tk.StringVar(self.window)
        self.mouse_menu_string.set("Reshape Wavefunction")
        self.mouse_menu = tk.OptionMenu(self.window,self.mouse_menu_string,*self.mouse_menu_tuple)
        self.mouse_menu.grid(row=8, column=3,columnspan=2,sticky=tk.W + tk.E + tk.N,padx=(10, 10))
        # Wavefunction entry field
        self.enter_function_label = tk.Label(self.window,text="Enter Wavefunction \u03C8(x)")
        self.enter_function_label.grid(row=9, column=3,columnspan=2,sticky=tk.E + tk.W + tk.S,padx=(10, 10))
        self.enter_function = tk.Entry(self.window)
        self.enter_function.bind("<Return>",self.updates_wavefunction_by_name)
        self.enter_function.grid(row=10, column=3,columnspan=2,sticky=tk.W + tk.E + tk.N + tk.S,padx=(11, 11))
        # updates probability button
        b = tk.Button(self.window,text='View Probability Distribution',command=lambda:[self.display_probability(),self.change_view.config(text='View Wavefunction')] if (self._display_probs is False) else [self.display_wavefunction(),self.change_view.config(text='View ''Probability'' Distribution')])
        self.change_view = b
        self.change_view.grid(row=1, column=3, columnspan=2, padx=(10, 10))
        # updates wavefunction button
        b2 = tk.Button(self.window, text='OK',command=self.updates_wavefunction_by_name)
        self.updates_wavefunction_button = b2
        self.updates_wavefunction_button.grid(row=11, column=3,columnspan=2,sticky=tk.N + tk.W + tk.E,padx=(10, 10))
        self.slider1 = []
        self.slider1_count = -1
        self.slider2 = []
        self.slider2_count = -1
        self.clear_wavefunction_button = None
        self.potential_menu_string = tk.StringVar(self.window)
        self.potential_menu = None
        self.enter_potential_label = None
        self.enter_potential = None
        self.updates_potential_button = None
        self.slider_speed_label = None
        self.slider_speed = None
        self.quit_button = None
        self.set_widgets_after_enter_wavefunction(init_call=True)
        self.animation_loop()
        # Store the animation speed before a pause
        self.fpi_before_pause = None
        self.scales_y = 0.0
        self.potential_is_reshaped = False


    def destroy_wavefunction_slider(self):
        """This method destroys the wavefunction parameter slider."""
        for slider in self.slider1:
            slider.destroy()
        self.slider1 = []
        self.slider1_count = 0


    def set_widgets_after_enter_wavefunction(self, init_call=False):
        """This method sets the widgets after the enter wavefunction button."""
        prev_slider1_count = self.slider1_count
        self.destroy_wavefunction_slider()

        if len(self.psi_params) > 0:
            for i in range(len(self.psi_params)):
                self.slider1.append(
                    tk.Scale(self.window, label="change %s: " % str(self.psi_params[i][0]),from_=-2, to=2,resolution=0.01,orient=tk.HORIZONTAL, length=200,command=self.updates_wavefunction_by_slider))
                self.slider1[i].grid(row=12 + self.slider1_count, column=3, columnspan=2, sticky=tk.N+tk.W+tk.E, padx=(10, 10))
                self.slider1[i].set(self.psi_params[i][1])
                self.slider1_count += 1
        if prev_slider1_count != self.slider1_count:
            self.set_widgets_after_wavefunction_slider(init_call)


    def set_widgets_after_wavefunction_slider(self, init_call):
        """This method sets widgets after wavefunction slider."""
        # Clear wavefunction button
        if self.clear_wavefunction_button is not None:
            self.clear_wavefunction_button.destroy()
        b3 = tk.Button(self.window,text='Clear Wavefunction',command=self.clear_wavefunction)
        self.clear_wavefunction_button = b3
        self.clear_wavefunction_button.grid(row=12 + self.slider1_count, column=3,columnspan=2,sticky=tk.W + tk.E,padx=(10, 10))
        # Potential function entry field
        if self.enter_potential_label is not None:
            self.enter_potential_label.destroy()
        self.enter_potential_label = tk.Label(
                self.window, text="Enter Potential V(x)")
        self.enter_potential_label.grid(row=14 + self.slider1_count,column=3,sticky=tk.W + tk.E + tk.S,padx=(10, 10))
        if self.enter_potential is not None:
            self.enter_potential.destroy()
        self.enter_potential = tk.Entry(self.window)
        self.enter_potential.bind("<Return>", self.updates_potential_by_name)
        self.enter_potential.grid(row=15 + self.slider1_count, column=3, columnspan=3,sticky=tk.W + tk.E + tk.N + tk.S,padx=(10, 10))
        if self.updates_potential_button is not None:
            self.updates_potential_button.destroy()
        b4 = tk.Button(self.window,text='OK',command=self.updates_potential_by_name)
        self.updates_potential_button = b4
        self.updates_potential_button.grid(row=16 + self.slider1_count, column=3,columnspan=2,sticky=tk.N + tk.W + tk.E,padx=(10, 10))
        if not init_call:
            params = [self.slider2[i].get() for i in range(len(self.slider2))]
            self.destroy_potential_slider()
            self.set_potential_slider()
            self.set_widgets_after_potential_slider()
            if len(params) != 0:
                for i in range(len(params)):
                    self.slider2[i].set(params[i])
                self.V = lambda x: self.V_base(x, *params)
                self.V_x = scales(self.V(self.x), 15)
                self.U_t = UnitaryOperation(self.V)
        else:
            self.set_widgets_after_enter_potential()


    def set_widgets_after_enter_potential(self):
        """This method sets the widgets after the enter potential button."""
        prev_slider2_count = self.slider2_count
        self.destroy_potential_slider()
        if len(self.V_params) > 0:
            self.set_potential_slider()
        if prev_slider2_count != self.slider2_count:
            self.set_widgets_after_potential_slider()


    def destroy_potential_slider(self):
        """This method destroys the potential slider"""
        for slider in self.slider2:
            slider.destroy()
        self.slider2 = []
        self.slider2_count = 0


    def set_potential_slider(self):
        """This method sets the slider for the parameters that controlthe potential function."""
        for i in range(len(self.V_params)):
            self.slider2.append(tk.Scale(self.window, label="change %s: " % str(self.V_params[i][0]),from_=-2, to=2,resolution=0.01,orient=tk.HORIZONTAL,length=200,command=self.updates_potential_by_slider))
            self.slider2[i].grid(row=17 + self.slider2_count + self.slider1_count, column=3, columnspan=2, sticky=tk.N+tk.W+tk.E, padx=(10, 10))
            self.slider2[i].set(self.V_params[i][1])
            self.slider2_count += 1


    def set_widgets_after_potential_slider(self):
        """This method sets the widgets after the parameter slider for the potential"""
        total_slider_count = self.slider2_count + self.slider1_count
        # Animation speed slider
        if self.slider_speed_label is not None:
            self.slider_speed_label.destroy()
        self.slider_speed_label = tk.LabelFrame(
                self.window, text="Animation Speed")
        self.slider_speed_label.grid(row=17 + total_slider_count,column=3, padx=(10, 10))
        if self.slider_speed is not None:
            self.slider_speed.destroy()
        self.slider_speed = tk.Scale(self.slider_speed_label,from_=0, to=10,orient=tk.HORIZONTAL,length=200,command=self.change_animation_speed)
        self.slider_speed.grid(row=18 + total_slider_count,column=3, padx=(10, 10))
        self.slider_speed.set(1)
        # Quit button
        if self.quit_button is not None:self.quit_button.destroy()
        self.quit_button = tk.Button(self.window, text='QUIT', command=self.quit)
        self.quit_button.grid(row=19  + total_slider_count, column=3)


    def mouse_wheel_handler(self, event):
        """This method handles mouse wheel input. When the mouse is over the canvasthis controls how the drawing of the potential is scalesd."""
        if event.delta == -120 or event.num == 5:
            self.rescales_potential_graph(1.1)
        elif event.delta == 120 or event.num == 4:
            self.rescales_potential_graph(0.9)


    def rescales_potential_graph(self, scales_y):
        """This method rescales the graph of the potential"""
        if not self.potential_is_reshaped:
            if np.amax(self.V_x > 0):self.scales_y = np.amax(self.V_x[1:-2])/(self.bounds[-1]*0.95)
            elif np.amax(self.V_x < 0):
                self.scales_y = np.abs(np.amin(self.V_x[1:-2]))/(self.bounds[-1]*0.95)
            else:
                self.scales_y = 1.0
            self.potential_is_reshaped = True
        self.scales_y *= scales_y
        self.lines[4].set_ydata(self.V_x/self.scales_y)


    def sketch(self, event):
        """This method responds to mouse interaction on the canvas."""
        if str(self.mouse_menu_string.get()) == self.mouse_menu_tuple[0]:
            self.updates_wavefunction_by_sketch_while_paused(event)
        elif str(self.mouse_menu_string.get()) == self.mouse_menu_tuple[1]:
            self.updates_wavefunction_by_sketch(event)
        elif str(self.mouse_menu_string.get()) == self.mouse_menu_tuple[2]:
            self.updates_potential_by_sketch(event)


    def updates_wavefunction_by_name(self, *event):
        """This method updates the wavefunction given entry input."""
        self.set_wavefunction(self.enter_function.get())
        self.set_widgets_after_enter_wavefunction()


    def _updates_wavefunction_by_sketch(self, x, y):
        """This method is a helper function for updates_wavefunction_by_sketch and updates_wavefunction_by_sketch_while_paused."""
        if not self._show_p:
            if self._display_probs:
                psi2_new = change_array(self.x, self.psi.x*np.conj(self.psi.x)/3, x, y)
                self.set_wavefunction(np.sqrt(3*psi2_new),normalize=False)
            else:
                self.set_wavefunction(change_array(
                    self.x, self.psi.x, x, y), normalize=False)
        else:
            if (x > self.x[self.N//4] and x < self.x[3*self.N//4]):
                if self._display_probs:
                    phases = np.angle(self.psi.p)
                    psi2_new = change_array(self.x, self.psi.p*np.conj(self.psi.p)/3, x, y)
                    psi_new = np.sqrt(3*psi2_new)*np.exp(1.0j*phases)
                    self.set_wavefunction(np.copy(np.fft.ifft(np.fft.ifftshift((psi_new)*(self.N/10)))), normalize=False)
                else: 
                    new_p = change_array(self.x, self.psi.p, x, y)
                    self.set_wavefunction(np.copy(np.fft.ifft(np.fft.ifftshift((new_p)*(self.N/10)))), normalize=False)


    def updates_wavefunction_by_sketch(self, event):
        """This method updates the wavefunction using the mouse."""
        x, y = self.locates_mouse(event)
        self._updates_wavefunction_by_sketch(x, y)


    def updates_wavefunction_by_sketch_while_paused(self, event):
        """This method updates the wavefunction with the mouse, while pausing the time evolution."""
        x, y = self.locates_mouse(event)
        if (str(event.type) == "Motion" or event.num != 1) and (self.fpi_before_pause is None):
            self.fpi_before_pause = self.fpi
            self.fpi = 0
        elif (str(event.type) == "ButtonRelease" or event.num == 1) and (
                self.fpi_before_pause is not None):
            self.fpi = self.fpi_before_pause
            self.fpi_before_pause = None
        self._updates_wavefunction_by_sketch(x, y)


    def clear_wavefunction(self, *args):
        """This method sets the wavefunction to zero."""
        self.set_wavefunction("0")


    def updates_potential_by_name(self, *event):
        """This method updates the potential using the potential entry input."""
        self.potential_is_reshaped = False
        self.potential_menu_string.set("Choose Preset Potential V(x)")
        self.previous_potential_menu_string = "Choose Preset Potential V(x)"
        no_prev_param_slider = True if len(self.V_params) == 0 else False
        self.set_unitary(self.enter_potential.get())
        if not no_prev_param_slider or len(self.V_params) > 0:
            self.set_widgets_after_enter_potential()


    def updates_potential_by_sketch(self, event):
        """This method updates the potential using the mouse."""
        if not self._show_p:
            x, y = self.locates_mouse(event)
            # This code block is reached right when the mouse is clicked and held down
            if (str(event.type) == "Motion" or event.num != 1) and (self.fpi_before_pause is None):
                # Get a scales for the y-coordinates in order for it to match up with the potential
                if not self.potential_is_reshaped:
                    if np.amax(self.V_x > 0):
                        self.scales_y = np.amax(self.V_x[1:-2])/(self.bounds[-1]*0.95)
                    elif np.amax(self.V_x < 0):
                        self.scales_y = np.abs(np.amin(self.V_x[1:-2]))/(self.bounds[-1]*0.95)
                    else:
                        self.scales_y = 1.0
                    self.potential_is_reshaped = True
                # Set the animation speed zero
                self.fpi_before_pause = self.fpi
                self.fpi = 0
                # Change the potential name to V(x)
                self.V_name = "V(x)"
                self.V_latex = "$V(x)$"
            # This code block is run right after the mouse has been held down
            elif (str(event.type) == "ButtonRelease" or event.num == 1) and (self.fpi_before_pause is not None):
                self.U_t = UnitaryOperation(np.copy(self.V_x))
                self.potential_menu_string.set("Choose Preset Potential V(x)")
                tmp_str = "Choose Preset Potential V(x)"
                self.previous_potential_menu_string = tmp_str
                # Resume the animation speed
                self.fpi = self.fpi_before_pause
                self.fpi_before_pause = None
            # This elif handles the case when mouse is clicked only once
            elif (str(event.type) == "ButtonRelease"
                or event.num == 1) and (self.fpi_before_pause is None):
                # Get a scales for the y-coordinates in order for it to match up with the potential
                if not self.potential_is_reshaped:
                    if np.amax(self.V_x > 0):
                        self.scales_y = np.amax(self.V_x[1:-2])/(self.bounds[-1]*0.95)
                    elif np.amax(self.V_x < 0):
                        self.scales_y = np.abs(np.amin(self.V_x[1:-2]))/(self.bounds[-1]*0.95)
                    else:
                        self.scales_y = 1.0
                    self.potential_is_reshaped = True
                self.V_x = change_array(self.x, self.V_x, x, y, gradual=False)
                self.V_name = "V(x)"
                self.V_latex = "$V(x)$"
                self.U_t = UnitaryOperation(np.copy(self.V_x))
                self.potential_menu_string.set("Choose Preset Potential V(x)")
                tmp_str = "Choose Preset Potential V(x)"
                self.previous_potential_menu_string = tmp_str
            # Re-draw the potential
            y *= self.scales_y
            self.V_x = change_array(self.x, self.V_x, x, y, gradual=False)
            if np.amax(self.V_x > 0):
                self.lines[4].set_ydata(self.V_x/self.scales_y)
            elif np.amax(self.V_x < 0):
                self.lines[4].set_ydata(self.V_x/self.scales_y)
            else:
                self.lines[4].set_ydata(self.x*0.0)


    def change_animation_speed(self, event):
        """This method changes the animation speed."""
        self.fpi = self.slider_speed.get()


    def locates_mouse(self, event):
        """This method locates the position of the mouse with respect to the coordinates displayed on the plot axes."""
        ax = self.figure.get_axes()[0]
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        pixel_xlim = [ax.bbox.xmin, ax.bbox.xmax]
        pixel_ylim = [ax.bbox.ymin, ax.bbox.ymax]
        height = self.canvas.get_tk_widget().winfo_height()
        mx = (xlim[1] - xlim[0])/(pixel_xlim[1] - pixel_xlim[0])
        my = (ylim[1] - ylim[0])/(pixel_ylim[1] - pixel_ylim[0])
        x = (event.x - pixel_xlim[0])*mx + xlim[0]
        y = (height - event.y - pixel_ylim[0])*my + ylim[0]
        return x, y


    def quit(self, *event):
        """This method quits the application."""
        self.window.quit()


if __name__ == "__main__":
    run = wave()
    tk.mainloop()