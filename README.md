[This project is a simulation of a single quantum particle inside a
bounded one-dimensional potential. It is a complex simulation that
relies on multiple course concepts.]{.mark}

Firstly, it relies on the concept of **code reuse**: the ability to use
existing code for a new function or program. The modular design of
programs massively helps in reusing codes. **Modular design** refers to
the idea of breaking down a large, complex system into smaller,
independent parts or modules: which are essentially collections of
functions. Once we import the module, we can easily use the things that
are defined inside the modules. I used object-oriented programming,
which is coding that relies on the concept of classes. Classes, in
simple terms, are blueprints for declaring and creating objects.
**Inheritance** of classes allows us to define a class that inherits all
the methods and properties from another class. Moreover, the parent
class is the class being inherited from and the child class is the class
that inherits from the parent class.

Through the use of these course concepts (and more: the NumPy, SciPy,
and Matplotlib libraries), I was able to effectively simulate the
quantum particle.

**[Project Description:]{.mark}**

[In this project, I have built a simulation app using Tkinter that lets
the user input the wave equation Ψ(x) and the potential V(x) for the
quantum particle: thus, allowing the user to manipulate the two values
for a quantum representation of the particle. For changing the wave, a
new wave function Ψ(x) could be typed into the 'Enter Wavefunction Ψ(x)'
entry box. The potential V(x) can also be changed accordingly.]{.mark}

[The default wave equation is:]{.mark}
$\ \Psi(x) = \ {e^{- 0.5(20(x - 0.25)^{2})}}^{}$ [and the potential
is]{.mark} $V(x) = {{2x}^{2}\ .}^{}$[I used NumPy (numerical
calculations), SymPy (symbolic computations), Matplotlib (graphing), and
Tkinter (GUI) throughout the project.]{.mark}

[Firstly, the dynamics of this quantum particle are given by the
equation:]{.mark}

> $|\ \Psi(t) > \  = \ U(t)\ *\ |\ \Psi(0) >$

[where: t is the time, \|Ψ(t)\> is the wavefunction vector of the
particle at time t, and U(t) is the unitary time evolution matrix. The
concept of unitary time evolution is used in this mechanics.]{.mark}

[Unitary time evolution is the specific type of time evolution where
probability is conserved. In quantum mechanics, one typically deals with
unitary time evolution. Physically, it means that the probability of the
existence of the quantum system does not change with time. The quantum
system exists at t=0 with probability=1, and also at t=T with
probability=1.]{.mark}

[The wavefunction vector \|Ψ(0)\> is a manipulated form of wave equation
Ψ(x) using the "WaveFunctionCreator" class. The wave function is
essentially represented in the form of Dirac Notation (Bra-Ket) through
integration and complex conjugation using the NumPy library.]{.mark}

[Similarly, the unitary time evolution matrix U(t) is a manipulated form
of the potential V(x) using the "UnitaryOperation" class. Essentially,
the potential is represented in the form of a matrix using zeros and
arrays from the NumPy library.]{.mark}

[The graph represents the wave function Ψ(x) and the potential V(x). But
the wave changes due to the quantum interactions that occur at each
instance; all of these dynamics were calculated earlier. Our particle is
set in a one-dimensional boundary along the X-axis from -0.5 to 0.5.
Every single unit used in this project (including the X-axis values) is
not a metric unit: they are natural units. All the fundamental constants
(Mass, Planck's constant, Charge) are set to 1. These constants are set
up into a \"constant\" class which is in the "collection" module. There
are also some other constants in this class required for setting up the
box in which the simulation takes place.]{.mark}

[The mouse can be used to draw a new shape for the wave function Ψ(x)
and the potential. To switch between reshaping the wave function and
potential, you can use the menu box on the GUI. Moreover, there's also
an option to change the wave function Ψ(x) in real-time i.e. the wave
values aren't saved and the wavefunction isn't paused when the reshaping
is taking place.]{.mark}

[The complex-valued wavefunction Ψ is not physically meaningful, because
the quantum world is hard to comprehend. Each particle is represented by
a wavefunction Ψ such that Ψ \* Ψ = the probability of finding that
particle at that position at that time. Thus, the probability density
(the probability distribution of where the particle may be found) can
also be viewed by clicking the "View Probability Distribution"
button.]{.mark}

[For time evolution, I have used "fpi" attribute, which is the number of
time evolution per animation frame. For the methods that pause time
evolution while receiving mouse input, the fpi_before_pause attribute
records the number of "fpi" right before the pause. This is then used to
set the "fpi" to the initial state (before the mouse button is
released). If the mouse is only clicked once, "fpi" wouldn't be
changing. Moreover, the "scales_y" attribute scales the y mouse input
values to match the proper scaling of the wave function or the
potential.]{.mark}

**[Instructions/Demonstration]{.mark}**

![](media/image1.png){width="6.5in" height="3.8333333333333335in"}

[To run the simulation, you have to run the file "main.py". You will get
a GUI interface that shows you the wave function for our particle along
the constraint -0.5\<x\<0.5. You will have entry boxes to enter new wave
equations and potential, a mouse drop-down menu to change the wave
equation or probability using the mouse, a view probability distribution
button that changes what is displayed (the wave function or the
probability density), and a quit button. The animation speed can be
adjusted using the slider. Note for the entry box: The default wave
equation is written as]{.mark} $\Psi(x) =$ [exp(-0.5\*(20\*x-5)\*\*2)
and the default potential is written as V(x) = 2\*x\*\*2.]{.mark}

[A wave function is a mathematical function (sin(x), exp(x),
cos(x\*\*2), etc). Like any mathematical function, it can have a large
value in some places, small in others, and zero elsewhere. It has a real
and complex component which is shown in our simulation through orange
and blue colors. This function contains all the information about a
system. If the wave function is large at a point in space, the particle
has a large probability of being found at that point. The more rapidly a
wavefunction changes from place to place, the higher the kinetic energy
of the particle it describes. Viewing the probability density allows us
to predict where our quantum particle could be along our one-dimensional
constraint.]{.mark}

**[Project Design Sketch:]{.mark}**

[The project comprises 4 modules: "main", "mechanics", "qmanimate", and
"collection".]{.mark}

[The "main" module utilizes Tkinter for creating a GUI for viewing and
interacting with the simulation. This is the main file for this project,
which primarily comprises the wave class. The "wave" class is run at the
end of the file and is a GUI representation of a quantum particle
bounded within a one-dimensional constraint. It is a child class that
inherits properties from the "Quantum" class of the "qmanimate" module.
Moreover, it uses the "WaveFunctionCreator" class and the
"UnitaryOperation" class of the "mechanics" module for carrying out the
quantum manipulations.]{.mark}

[The "qmanimate" module uses Matplotlib for the creation of graphs. It
primarily comprises the "Quantum" class which is essentially where all
the lines are graphed after parsing the input. This class is also a
child class of the \"constant\" class of the "collection" module. It
uses the "Function" class of the "collection" module to manipulate and
parse the functions. Moreover, it also uses the "WaveFunctionCreator"
class and the "UnitaryOperation" class of the "mechanics" module for
carrying out the quantum manipulations.]{.mark}

[The "mechanics" module is responsible for the actual quantum physics in
this project. It consists of two classes: "WaveFunctionCreator" and
"UnitaryOperation". "WaveFunctionCreator" class uses the Fourier
transform process to decompose our wave function into real and imaginary
parts (using NumPy) such that the wave function can be then integrated
and represented in the form of a vector ket. Whereas the
"UnitaryOperation" class helps us evolve time for our quantum simulation
such that the input potential is transformed into matrices using the
Numpy library.]{.mark}

[The "collection" module is a collection of various functions and
classes that are used in other modules of this program. It has the
\"constant\" class, which is essentially the parent class for almost all
of our other classes. This class standardizes the natural units and sets
their values. Moreover, this module also has the "Function" class, which
helps in manipulating the functions entered by the user for
graphing.]{.mark}

[A Rough Project Design Image that includes all the classes:]{.mark}

![](media/image2.png){width="6.5in" height="4.5in"}

[Note: As my project has a total of 54 methods/functions, the sketch
incorporating the interactions between all of them would be way too
convoluted.]{.mark}


[As an extension for this project, I added the option for the user to
change the wave function Ψ(t) (in real-time) and potential V(x) for our
simulation using the mouse. There is a drop-down menu labeled 'Mouse:',
which allows the user to toggle between the different options.]{.mark}

[For instance, when the mouse click is registered on the graph, it is
recorded as a boolean. Then the simulation will be paused until the
mouse click is released, thus allowing the potential V(x) to be changed.
This then changes the quantum attributes of the particle, in turn
changing the simulation entirely. The 'potential_is_reshaped' bool
attribute notifies the method 'updates_potential_by_sketch' whether the
potential has been changed by the mouse input. This is so that the
potential isn't rescaled (through changing the y-attribute) whenever the
'updates_potential_by_sketch' is called more than once. This attribute
is set to false when 'updates_potential_by_name' is called. Similarly,
the attribute is also set to false when the wave function is being
changed; but when the wave function is being changed in real-time, this
attribute is set to true, such that the wave is getting updated every
single instance of 'fpi'.]{.mark}


**[Potential Biases or Limitations:]{.mark}**

[As noted earlier, this is a one-dimensional simulation of a unit
quantum particle. The constraint setup (-0.5\<x\<0.5) is also in a
single dimension. Hence, it would be ideal for the simulation to be
extended to higher dimensions such that the quantum dynamics could be
explored even further. At the moment, I am yet to understand the
complexities and intricacies that are involved in higher dimensions,
which means that this project is slightly limited in that regard.
Moreover, my programming skills may also be inadequate (and in fact, my
machine may be inadequate) to further this simulation into an unlimited
quantum dimension. However, I believe that learning the probabilistic
distribution of a quantum particle even in a single dimension is a hefty
analysis that allows us to rejoice in this physical phenomenon.
Moreover, the project does not work as expected for very high energy
values, which also limits this simulation to a certain extent. A further
analysis and time commitment (and further knowledge of Quantum
mechanics) would be essential for emboldening this simulation.]{.mark}
