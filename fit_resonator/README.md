# Python Code to Fit Microwave Resonator Data
>Keegan Mullins (CU Boulder NIST Affiliate)
Corey Rae McRae (NIST)
Haozhi Wang (NIST)
Josh Mutus (Google)

#### This code is a modified version of the original code written by:

>Kevin Osborn (University of Maryland, LPS)
Chih-Chiao Hung (University of Maryland, LPS)

## Starting Notes

This code is made to fit complex S21 data for hangar type resonators using the Diameter Correction Method (DCM), Inverse S21 method (INV), Closest Pole and Zero Method (CPZM), and Phi Rotation Method (PHI) fittings

Additionally, the code is able to fit reflection type geometry resonators with an altered version of the Diameter Correction Method (DCM REFLECTION)

1. DCM: M. S. Khalil, M. J. A. Stoutimore, F. C. Wellstood, and K. D. Osborn    Journal of Applied Physics 111, 054510 (2012); doi: 10.1063/1.3692073
1. INV: A. Megrant et al.     APPLIED PHYSICS LETTERS 100, 113510 (2012)
1. CPZM: Chunqing Deng, Martin Otto, and Adrian Lupascu University of Waterloo, Waterloo, Ontario N2L 3G1, Canada (9 August 2013)
1. PHI: J. Gao, "The Physics of Superconducting Microwave Resonators" Cal-tech Ph.D. thesis, May 2008

## Fitting Functions:
![alt text](https://raw.githubusercontent.com/Boulder-Cryogenic-Quantum-Testbed/measurement/master/fit_resonator/Fit_Equations.PNG)

## INPUT:
The code takes in a file (currently accepts .snp .csv and .txt files). If the file is a .snp file it should follow the .snp format. If the file is a .csv or .txt it should contain 3 columns separated by commas where each line represents one point of data.
   >Headers are not accepted in the file .csv and .txt files, the code only accepts the data with a header for .snp

Format for .csv and .txt files:

1. The first column is monotonically increasing frequency in GHz
1. The second column is magnitude of S21 in dB (log mag)
1. The third column is phase of S21 in degrees
   >More information regarding standard data format can be found here https://github.com/Boulder-Cryogenic-Resonator-Testbed/measurement/issues/19

The user has the option of including a background removal file in order to have a more accurate fit. This is recommended if the background is not linear.
   >Background file needs to be of the same format as the main data file as described with the three columns above.

User needs to ensure that the data has at least 20 points otherwise the code will fail

If user does not include points near off resonance in addition to points near resonance, fitting will not be accurate and could fail entirely
   >In simple terms: The fitting needs a full circle (in complex plane) to work optimally

## OUTPUT:

All output will be put in a new folder titled with a timestamp in the folder with the user's data.

1. If the user has a background removal file, the code will output graphs displaying the main data and the background for both the magnitude and phase
1. The code will output four figures showing the steps it is taking to normalize the data titled Normalize_1 through Normalize_4
1. If the user opted to have the code guess initial parameters, the code will output three figures showing the steps taken to find resonance and phi guesses
1. The code outputs a figure displaying a variety of information regarding how the fit was completed. This includes a plot of both the raw and final fit of data
in the complex plane, plots of the linear fits that normalize the data for both magnitude and phase, plots of the normalized magnitude and phase with their final
fits, manually input guess parameters, and the final parameters found from the fit with their 95% confidence intervals.
1. The code will also print a .csv file displaying the information that the fit has gathered with each term on a new line:
    * DCM/DCM REFLECTION/PHI: Q, Qi, Qc, 1/Re[1/Qc], phi, f_c
    * INV: Qi, Qc*, phi, f_c
    * CPZM: Qi, Qc, Qa, f_c

>User has the option of disabling extra graphs such as the normalization process graphs when calling the fit_resonator function

-----------------------------------------------------------------------------------

## Code Overview

1. From user python file, code takes in user data file name along with the associated directory and passes it to Fit_Resonator function along with user preferences and an optional background removal file name
1. If user has a background file, the code will use it to remove the background for a more accurate fit
1. Data is pre-processed using a linear fit for both magnitude and phase of S21 so that start and end points of S21 data are at (1,0i) in the complex plane
1. If the user does not manually initialize a guess, the code will attempt to find a guess for fit parameters using Find_initial_guess function
1. Once the code has a guess for fit parameters, it will crop the data to points near resonance
1. After cropping, the code will minimize the guess parameters based on data points using a least squares fit then compare parameters to a Monte Carlo fit
   >This step will be repeated until the Monte Carlo fit does not give better results than the minimization.
   >Monte Carlo fit is meant to check if fitting parameters are trapped in a local minimum.
   >If Monte Carlo fit got better results, the parameters obtained from Monte Carlo fit will be minimized.

1. The 95% confidence interval is found for the fit and the range of values for the interval is reported as the error in the final plot
1. At this point the final parameter values have been found and fitting is complete. Final fitting is plotted and fit parameters are written to a .csv file

-------------------------------------------------------------------------------------------------------------------------------------------------------------

## Installation

User will need the following python modules:
* attr
* inflect
* lmfit
* matplotlib
* numpy
* pandas
* scipy
* sympy

To install these modules, the user can run the following command from the measurement directory:

`pip install -r requirements.txt`

> Alternatively to the requirements.txt, user can install a module with "pip install ______" on the command line for python 3.
Must install pip module before installing pips for python 2. Once pip is installed for python 2, install modules the same way as python 3.

-------------------------------------------------------------------------------------------------------------------------------------------------------------

## Using the code

###### An example of the way the following is done is included in the main README

#### Section 1: Initial Setup
Import code library with:
`import fit_resonator.resonator as scres`
###### User will need to set a variable with the name of their file:
###### OR have a variable containing their raw data

#### Section 2: Setting Fit Variables

###### User must initialize a Fit_Method class instance with arguments: 
* fit_type
* MC_iteration
* MC_rounds
* MC_fix
* manual_init
* MC_step_const

fit_type: 'DCM','DCM REFLECTION','PHI','INV' or 'CPZM' for the method user wishes to run

MC_iteration: The number of times the user wants the Monte Carlo fit to run

MC_rounds: The number of iterations the Monte Carlo fit will do per run. Default is 100 if not defined

MC_fix: An array of which variables the MC fit will not change during iteration.
   >An example of MC_fix is as follows:
   `MC_fix = ['w1','Qi']`
   >The strings user can use for MC_fix are as follows: 'Q','Qi','Qc','w1','phi','Qa'

manual_init: Used to define initial guess variables
   >If the user wants to have the program auto guess parameters, they can set manual_init equal to None
   
   >If the user wants to define their own initial guess parameters, they must define it in the following format: 
   `manual_init = [1,2,3,4]`
    1 = Qi
    2 = Qc
    3 = resonance frequency (GHz)
    4 = phi (radians) or Qa (Qa only used for CPZM)

> Note that if using CPZM, 4 needs to be Qa not phi. If using any other method, 4 needs to be phi.

MC_step_const: Range for the random parameter values chosen in MC fit. This scaling is exponential. The larger this number, the higher and lower the random values

#### Section 3: Fitting Data

Initialize resonator object with:
`my_resonator = scres.Resonator()`

Initialize raw data or file into resonator object with:
`my_resonator.from_columns(raw_data)`
`my_resonator.from_file(filename)`

You can also pass the data as a filename or data object when initializing your resonator object with:
`my_resonator = scres.Resonator(filepath='PATH/TO/FILE')`
`my_resonator = scres.Resonator(data=raw_data)`

If you're using a snp file with more than three columns please specify to the resonator object which value to use with:
`my_resonator.from_file('PATH/TO/FILE.snp', "S12")`
`my_resonator = scres.Resonator(filepath='PATH/TO/FILE.snp', measurement="S12")`
or with the index value(s)
`my_resonator.from_file('PATH/TO/FILE.snp', [2,3])`
`my_resonator = scres.Resonator(filepath='PATH/TO/FILE.snp', measurement=[2,3]`


Define the parameters of your fitting method with:
my_resonator.fit_method(method: str,
MC_iteration=None,
MC_rounds=100,
MC_weight='no',
MC_weightvalue=2,
MC_fix=[],
MC_step_const=0.6,
manual_init=None):)

Call the fitting function once resonator class hold all relevant information with:
`params1,fig1,chi1,init1 = my_resonator.fit()`

If the user wants to have the code remove their background, they need to include the path to their background removal file in resonator object initialization with:
`my_resonator = scres.Resonator(background = background_file)`
For scaling file data and background file data
`my_resonator.from_file(filepath, fscale)`
`my_resonator.init_background(filepath, fscale)`

normalize: The number of points from the start/end of S21 data the user wants to use in the linear fit of S21 data for magnitude and phase for normalization, set with:
`my_resonator = scres.Resonator(normalize = integer value)`

Remember for these special initializations you can include as many as you need, just don't forget the keyword arguments!
`my_resonator = scres.Resonator(background = background_file, normalize = 5, filepath = "PATH/TO/FILE, measurement = "S21")`

##Check Data:

A simple script to detect if the user's data file is of the correct format.

To use, simply change the path variables dir to directory with file, and filename to the name of the file to be checked.

To use, import the module:

`import fit_resonator.check_data as cd`

Then run the method corresponding to your data form as a file, or raw data as arrays/array-likes:

`cd.file(path_to_data_file)`

`cd.raw(frequency, magnitude, phase)`

This code will check data files for:
* Header (not currently part of standard format)
* Correct number of columns
* Correct delimiter (currently set to ',')

Files and raw data for:
* Containing more than 1 line of data
* Frequency in GHz (determined by checking if frequency is above 10^8 in magnitude)
* Phase in radians (determined by checking if phase less/greater than 2pi)

>Code does not check if magnitude is in dB

The code will prompt the user to check if they would like to make a new file with an edited version of their data using the correct format for each individual change.
