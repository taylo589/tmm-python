#!/usr/bin/env python2.7
'''
TMM: main.py - Luke's python transfer-matrix method (ala Pochi Yeh's method)

04/10/2015 - LNT - first. attempt to object-orient the code. system oriented around 
                    a custom prompt system. would like to add refractive-index.info's
                    database support (YAML comprehension)

TODO:
  * add wavelength
'''
# import simple gui for file choosing
from Tkinter import Tk
from tkFileDialog import askopenfilename
from TMM_Util import *
import numpy as np

# a class defining each layer
class TMM_Layer:
  def __init__(self,refrindex,othickness,NAME=''):
    self.n = refrindex
    self.nd = othickness
    self.DESC = \
        "{0}. Refractive Index: {1:f}. Thickness: {2:f} wavelengths"\
        .format(NAME,refrindex,othickness)

    self.D = get_D(self.n) # from TMM_Util
    self.P = get_P(self.nd)
    self.invD = invABCD(self.D)

# a class defining the substrate
class TMM_Substrate:
  def __init__(self,refrindex,NAME='Substrate'):
    self.n = refrindex
    self.DESC = "{0}. Refractive Index: {1:f}."\
        .format(NAME,refrindex)

    self.D = get_D(self.n)

# a class defining the medium
class TMM_Medium:
  def __init__(self,refrindex,NAME='Medium'):
    self.n = refrindex 
    self.DESC = "{0}. Refractive Index: {1:f}."\
        .format(NAME,refrindex)

    self.D = get_D(self.n)
    self.invD = invABCD(self.D)

# this is the total system class
class TMM_System:
  def __init__(self):
    self.layers = []
    self.medium = None
    self.substrate = None

  def add_medium(self,medium):
    self.medium = medium
    return

  def add_substrate(self,substrate):
    self.substrate = substrate
    return

  def add_layer(self,layer):
    self.layers.append(layer)
    return

  def calc_system(self):
    M = self.substrate.D
    for layer in self.layers:
      M = multABCD(layer.invD,M)
      M = multABCD(layer.P,M)
      M = multABCD(layer.D,M)

    M = multABCD(self.medium.invD,M)
    self.Msys = M
    self.r = M[2]/M[0]
    self.t = 1./M[0]
    self.R = (abs(self.r))**2
    self.T = (abs(self.t))**2*(self.substrate.n/self.medium.n)

def load_file(filename):
  print "not yet"

# layer loop (note, layers should be entered substrate-up, just like they are grown)
# so layers[0] should refer to the layer closest to the substrate
def layer_loop(tmm_system):
  i = 0
  LAYER_ENTRY = True
  while(LAYER_ENTRY):

    # get index
    ni = index_loop(i)

    # get thickness
    ndi = thickness_loop(i)

    # make a layer
    layer_i = TMM_Layer(ni,ndi)

    # add the layer to the system
    tmm_system.add_layer(layer_i)

    # next layer
    print "Another layer? [y],n"
    next_decision = raw_input()
    if next_decision == 'n':
      LAYER_ENTRY = False
    else:
      i += 1

  return

# layer refractive index
def index_loop(i):
  INDEX_ENTRY = True
  while(INDEX_ENTRY):
   print "Enter the refractive index of the layer:"
   ni = raw_input('[layer {0}]: '.format(i))
   if ni == '':
     print "No refractive index entered..."
   else:
     INDEX_ENTRY = False
  return float(ni)

# layer thickness
def thickness_loop(i):
  THICK_ENTRY = True
  while(THICK_ENTRY):
    print "Enter the optical thickness (nd) of the layer in wavelengths:"
    ndi = raw_input('[layer {0}]: '.format(i))
    if ndi == '':
      print "No thickness entered..."
    else:
      THICK_ENTRY = False
  return float(ndi)

def load_interactive():

  # instantiate the system class
  tmm_sys = TMM_System()

  # enter the relative wavelegth range
  print "Enter the relative wavelegth range (default: 1.0) [START END POINTS]:"
  wl_input = raw_input('[wavelength]: ')
  try:
    wl_range = tuple(float(x.strip()) for x in wl_input.split(' '))
    wl = np.linspace(*wl_range)
  except ValueError:
    wl = 1.0
  except:
    print "Invalid wavelength range entered. Returning to start."
    return

  # starting medium
  print \
"Enter the refractive index of the starting medium: REAL,[COMPLEX] (default: air, n = 1)."
  n0 = raw_input('[medium]: ')
  if n0 == '':
    tmm_med = TMM_Medium(1.)
  else:
    tmm_med = TMM_Medium(float(n0))
  tmm_sys.add_medium(tmm_med)

  # substrate 
  print \
"Enter the refractive index of the substrate: REAL,[COMPLEX] (default: silicon, n = 3.41)."
  nS = raw_input('[substrate]: ')
  if nS == '':
    tmm_sub = TMM_Substrate(3.41)
  else:
    tmm_sub = TMM_Substrate(float(nS))
  tmm_sys.add_substrate(tmm_sub)


  # go thru and get the layers now (pass the tmm_sys object)
  layer_loop(tmm_sys)

  # do the calculation
  print "Calculating system matrix"
  tmm_sys.calc_system()

  #print or whatever
  print "Calculation Complete"
  print "R = {0}, T = {1}, A = {2}."\
      .format(tmm_sys.R,tmm_sys.T,1.-tmm_sys.R-tmm_sys.T)


def tmm_loop():
  # Define Mode of operation (interactive vs. file-based)
  print '\n'
  print "***************************************************************"
  print "How would you like to use the code?"
  print "***************************************************************"
  QUIT = False

  # Main code loop
  while(not QUIT):
    print "Hit \'f\' for file-based or \'i\' for interactive [Default]. Hit \'q\' to quit."
    mode = raw_input('[mode]: ')

    # mode comprehension logic
    # file mode
    if mode == 'f':
      # we don't want a full GUI, so keep the root window from appearing
      Tk().withdraw() 
      # show an "Open" dialog box and return the path to the selected file
      filename = askopenfilename() 
      print(filename)
      load_file(filename)

    # interactive mode
    elif mode == 'i' or mode == '':
      load_interactive()

    # quitting mode :-)
    elif mode == 'q':
      QUIT = True
      break
    else:
      print "Mode type not understood\n"

    # decide whether or not to keep going
    print "Program Finished. Hit \'q\' to quit or [ENTER] to continue"
    cont = raw_input('[cont?]:')

    if cont == 'q':
      QUIT = True

# Main code if executed as script
if __name__ == '__main__':

  # Welcome Message
  print "***************************************************************"
  print "***************************************************************"
  print "Transfer Matrix Method Calculation Code in Python with NumPy."
  print "Based on Pochi Yeh's method from \"Optical Waves in Layered Media\""
  print "with add'l work by Joseph Talghader, Anand Gawarikar, Kyle Olsen and Luke Taylor"
  print "***************************************************************"
  print "***************************************************************"
  
  # Main program loop:
  tmm_loop()

