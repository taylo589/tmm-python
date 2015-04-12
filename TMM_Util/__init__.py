'''
TMM_Util
__init__.py - utility functions for the transfer matrix method

4/12/2015 - LNT - from Anand Gawarikar's "multilayered.m"
'''
import numpy as np

# D- matrix (start w/ just s-wave)
def get_D(n,theta=0.):
  D_11 = 1.
  D_12 = 1.
  D_21 = n*np.cos(theta)
  D_22 = -n*np.cos(theta)
  return D_11,D_12,D_21,D_22

# P- matrix (assume d is optical thickness already normalized by lambda)
def get_P(nd,theta=0.):
  phi = 2.*np.pi*nd*np.cos(theta)
  P_11 = np.exp(1j*phi)
  P_12 = 0.
  P_21 = 0.
  P_22 = np.exp(-1j*phi)
  return P_11,P_12,P_21,P_22

# calculates a matrix inverse for our abcd structure
def invABCD(ABCD):
  A = ABCD[0]
  B = ABCD[1]
  C = ABCD[2]
  D = ABCD[3]
  N = 1./(A*D-B*C)
  Ai = N*D
  Bi = -N*B
  Ci = -N*C
  Di = N*A
  return Ai,Bi,Ci,Di

# multiplies two 2x2 matricies together (so they can hold big datas in other dims!!)
def multABCD(ABCD1,ABCD2):
  Am = ABCD1[0]*ABCD2[0] + ABCD1[1]*ABCD2[2]
  Bm = ABCD1[0]*ABCD2[1] + ABCD1[1]*ABCD2[3]
  Cm = ABCD1[2]*ABCD2[0] + ABCD1[3]*ABCD2[2]
  Dm = ABCD1[2]*ABCD2[1] + ABCD1[3]*ABCD2[3]
  return Am,Bm,Cm,Dm

