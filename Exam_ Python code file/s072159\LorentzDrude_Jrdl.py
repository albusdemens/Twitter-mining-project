__version__ = 1.0
__author__ = "Jakob Rosenkrantz de Lasson"

# This script defines the Python function LorentzDrude(lambda0,material) which calculates the (relative) electric permittivity, epsilon,
# of the material 'material' (which can be either 'Ag' (silver) or 'Au' (gold)) at the wavelength 'lambda0' 
# (which can be either a scalar or a vector). The function returns the calculated permittivities which in general are complex numbers.
# After defining the function, a call of the function is performed, and the calculated permittivities are printed.

# The permittivity is described using the so-called Lorentz-Drude model, which takes both inter- and intraband transitions in the considered
# material into account; the details of the model and the involved parameters are described in the article
# A. D Rakic et al., "Optical properties of metallic films for vertical-cavity optoelectronic devices" 
# (download the article at http://www.opticsinfobase.org/ao/abstract.cfm?id=61190)

from numpy import *
import math

# Define the function LorentzDrude
def LorentzDrude(lambda0,material):
	# Define material independent constants
	pi = math.pi # Define pi
	c = 299792458 # Velocity of light in vacuum in units m/s
	hbar = 4.135667516e-15/(2*pi) # Planck's reduced constant in units eV*s
	lambda0m = lambda0*1e-6 # Wavelength in units m
	omega = 2*pi*c/(lambda0m) # Frequency in units of radians/s

	if material=='Ag': 
		# Define 'Ag' (silver) parameters in the Lorentz-Drude permittivity model
		omegap=9.01/hbar
		f0=0.845
		Omegap=sqrt(f0)*omegap
		Gamma0=0.048/hbar
		f=array([0.065, 0.124, 0.011, 0.840, 5.646])
		Gamma=array([3.886, 0.452, 0.065, 0.916, 2.419])/hbar
		omega_n=array([0.816, 4.481, 8.185, 9.083, 20.29])/hbar
	elif material=='Au': 
		# Define 'Au' (gold) parameters in the Lorentz-Drude permittivity model
		omegap=9.03/hbar
		f0=0.760
		Omegap=sqrt(f0)*omegap
		Gamma0=0.053/hbar
		f=array([0.024, 0.010, 0.071, 0.601, 4.384])
		Gamma=array([0.241, 0.345, 0.870, 2.494, 2.214])/hbar
		omega_n=array([0.415, 0.830, 2.969, 4.304, 13.32])/hbar

	# Initialize interband contributions to permittivity
	epsInter = 0 

	# Loop over Lorentz-type terms that constitute the interband contributions
	for fval,Gammaval,omega_nval in zip(f,Gamma,omega_n):
		epsInter=epsInter+fval*omegap**2/(omega_nval**2-omega**2+1j*omega*Gammaval)

	# Calculate intraband contribution to the permittivity
	epsIntra = 1-Omegap**2/(omega*(omega-1j*Gamma0))
	 # Sum inter- and intraband contributions to permittivity to have the total permittivity
	epsilon = epsIntra+epsInter
	# Return the calculated permittivity epsilon
	return epsilon

# Example call of the defined function LorentzDrude
epsilonCalculated = LorentzDrude(linspace(0.5,0.6,20),'Ag')
# Print calculated permittivites
print(epsilonCalculated)

