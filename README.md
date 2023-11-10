# TSTORM_communication_enabled
# write in 2023
this is the hardware-control software for a TSTORM microscope system built at USTC.

# write in 2018

this is the newest version of TSTORM software. 

synchronous between hardwares is accomplished through queue

issues:
  
  1.when file excesses 10G, recording speed is not enough,but this is the issue shared by most tiff_writer methods
  
  2.shutter, I think it's hardware issue rather than software issue. the port on the DAQ card seems not to support single output
  
  3.SLM part
  
  4.AO part
