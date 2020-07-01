Created in 2014 during my doctoral research
Verified and uploaded 7/1/2020

The file "ellipsometry-SOC.py" was written to take the data output of an ellipsometer and calculate the stress-optic coefficient of the glass being tested. 

A bit about the science, methods, and files:
- The ellipsometer measurements were taken in "transmission mode", i.e. the light source incident on the detector. The equipment would output a "Delta" value, which was the angular difference between horizontally polarized and vertically polarized light. This value essentially tells you what the polarization of light leaving the sample is. 
- Samples were held between the light source and the detector, and stress was applied uniformly along one axis. For each stress applied, an ellipsometer measurement (.dat file) was taken.
- For each composition considered, repeat measurements of samples were taken, and multiple samples were tested.
- Knowing the wavelength, the Delta value and the applied stress, the stress-optic coefficient can be calculated. 

Because so many sample sets were used, I wanted to create a script that would automatically go through each set, calculate the SOC for each wavelength, and then take the average and standard deviation for all of the sample sets. This resulted in "ellipsometry-SOC.py". This script outputs a file with three columns --  wavelength, SOC avg, SOC error -- which is automatically given the name of the main folder. 

To function properly, the following must be true:
- there must be a file called "dim" in the main folder that contains the sample dimensions
- each data set must be contained in its own folder within the main folder

I'm going to upload and try to include some sample data, so that the full functionality is here. Defining equipment and compositional notes have been removed. 

