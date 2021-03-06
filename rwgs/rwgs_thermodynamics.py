from numpy import *
from scipy.optimize import *
import random
#from sympy.core.symbol import symbols
#from sympy.solvers.solveset import nonlinsolve

R = 8.3145 #J/mol/K
T = 600 + 273.15 #K
P = 1.01325*10**5 #J/m^3
n0 = {'CO2': 1, 'H2': 3, 'CO': 0, 'H2O': 0, 'CH4': 0} #kmol

#std Gibbs FE of formation
Gf = {'CO2': -394.38, 'H2': 0, 'CO': -137.16, 'H2O': -228.614, 'CH4': -50.45}
#rxn1: Reverse Water Gas Shift
G1 = Gf['CO'] + Gf['H2O'] - Gf['CO2'] - Gf['H2']
#rxn2: Methanation
G2 = Gf['CH4'] + Gf['H2O'] - Gf['CO'] - 3*Gf['H2']
#rxn3: the Sabatier rxn
G3 = Gf['CH4'] + 2*Gf['H2O'] - Gf['CO2'] - 4*Gf['H2']

#Calculating equilibrium constants K1, K2, and K3
K1 = exp(-G1/R/T)
K2 = exp(-G2/R/T)
K3 = exp(-G3/R/T)

def GasEq(zeta):
    #z = extent of rxn (kmol)
    z1 = zeta[0]
    z2 = zeta[1]
    z3 = zeta[2]
    print(zeta)

    #Moles
    n = {}
    n['H2']  = n0['H2']  - z1 - 3*z2 - 4*z3
    n['CO2'] = n0['CO2'] - z1 - z3
    n['CO']  = n0['CO']  + z1 - z2
    n['H2O'] = n0['H2O'] + z1 + z2 + 2*z3
    n['CH4'] = n0['CH4'] + z2 + z3

    ntot = 0
    for key in n:
        ntot = ntot + n[key]
    y = {}
    for key in n:
        y[key] = n[key] / ntot


    #for key in y:
    #    if y[key] < 0:
    #        y[key] = 0;

    #system of equations
    print(y)
    E = [0]*3
    E[0] = y['CO']*y['H2O']/y['CO2']/y['H2'] - K1
    E[1] = 1/(P**2)*y['CH4']*y['H2O']/y['CO']/(y['H2']**3) - K2
    E[2] = 1/(P**2)*y['CH4']*(y['H2O']**2)/y['CO2']/(y['H2']**4) - K3
    return E

zetaGuess = array([random.uniform(.1,.2), random.uniform(0,.1), random.uniform(0,.3)])

zeta = root(GasEq, zetaGuess, tol=0.1)
print(zeta)
