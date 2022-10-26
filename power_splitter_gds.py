"""
layout for 2x2 50:50 power splitter exercise
"""
#import numpy as np

import nazca as nd
import nazca.demofab as demo

#some variables
fiber_pitch = 127
# clear layers
nd.clear_layers()
print("Running Nazca version " + nd.__version__)


file_name = 'power_splitter'

### Part 1: define a cross-section with proper layers ###
#########################################################

# create a xsection
nd.add_xsection(name='xs1') #  -- channel waveguide

# create layers
nd.add_layer(name='L1', layer=1, accuracy=0.001)

# combine layers in a xsection
nd.add_layer2xsection(xsection='xs1', layer='L1')


### Part 2: use pre-defined interconnects ###
#############################################

# create an interconnect object
ic1 = nd.interconnects.Interconnect(xs='xs1')
ic1.radius = 20 #default bend radius
ic1.width = 0.5 #default wire width

### Part 3: use BBs ###
#######################
def splitter(coupling_length = 8.17, gap = 0.12):
    offset = 10
    with nd.Cell('parametric_splitter') as bb:
        input1 = ic1.strt(length=5).put(0,0)
        ic1.sbend(offset = -offset).put()
        ic1.strt(length=coupling_length).put()
        ic1.sbend(offset = offset).put()
        output1 = ic1.strt(length=5).put()
        
        input2 = ic1.strt(length=5).put(0,-(offset*2+gap+ic1.width))
        ic1.sbend(offset = offset).put()
        ic1.strt(length=coupling_length).put()
        ic1.sbend(offset = -offset).put()
        output2 = ic1.strt(length=5).put()
        
        nd.Pin('a0').put(input1.pin['a0'])
        nd.Pin('a1', pin=input2.pin['a0']).put()
        nd.Pin('b0', pin=output1.pin['b0']).put()
        nd.Pin('b1', pin=output2.pin['b0']).put()
        nd.put_stub()      
    return bb

with nd.Cell('grating_coupler') as gc:
    swg_pitch = 0.45
    number_of_swg_period = 30
    number_of_period = 25
    swg_hole_width = 0.171
    dc_z = 0.55
    pitch_z = 0.81
    taper_length = 20
    taper_final_width = number_of_swg_period*swg_pitch+(swg_pitch-swg_hole_width)
    taper = ic1.taper(length=taper_length, width2=taper_final_width).put()
    for kk in range(number_of_swg_period+1):
        ic1.strt(length=(number_of_period-1)*pitch_z+pitch_z*(1-dc_z), width=swg_pitch-swg_hole_width).put(taper_length+pitch_z*dc_z,taper_final_width/2-swg_pitch*kk-(swg_pitch-swg_hole_width)*0.5)
    for kk in range(number_of_period+1):
        ic1.strt(width=taper_final_width,length=pitch_z*dc_z).put(taper_length+pitch_z*kk)
    nd.Pin('a0').put(taper.pin['a0'])
    
with nd.Cell('wg_term') as wt:
    wg_term = ic1.taper(length=10,width1=0.5,width2=0.1).put()
    nd.Pin('b0').put(wg_term.pin['b0'])

#placing grating couplers
gc_list  = []
for kk in range(10):
    gc_list.append(gc.put(0,kk*fiber_pitch,180))
    
gc_list2  = []
for kk in range(8):
    gc_list2.append(gc.put(kk*fiber_pitch+200,0,-90))
    
gc_list3  = []
for kk in range(10):
    gc_list3.append(gc.put(kk*fiber_pitch+200,250,-90))
    
gc_list4  = []
for kk in range(10):
    gc_list4.append(gc.put(kk*fiber_pitch+200,500,-90))
    
gc_list5  = []
for kk in range(10):
    gc_list5.append(gc.put(kk*fiber_pitch+200,750,-90))
    
gc_list6  = []
for kk in range(10):
    gc_list6.append(gc.put(kk*fiber_pitch+200,1000,-90))
    
gc_list7  = []
for kk in range(9):
    gc_list7.append(gc.put(kk*fiber_pitch+200,1250,-90))
    
#insertion loss test 1
insertion_connect1 = ic1.strt(length=20).put(gc_list[0].pin['a0'])
insertion_connect2 = ic1.strt(length=20).put(gc_list[1].pin['a0'])
insertion_connect_1_2 = ic1.strt_bend_strt_p2p(pin1 = insertion_connect1, pin2 = insertion_connect2).put()

#insertion loss test 2
insertion_connect3 = ic1.strt(length=20).put(gc_list[2].pin['a0'])
insertion_connect4 = ic1.strt(length=20).put(gc_list[3].pin['a0'])
insertion_connect_3_4 = ic1.strt_bend_strt_p2p(pin1 = insertion_connect3, pin2 = insertion_connect4).put()

#insertion loss test 3
insertion_connect5 = ic1.strt(length=20).put(gc_list[4].pin['a0'])
insertion_connect6 = ic1.strt(length=20).put(gc_list[5].pin['a0'])
insertion_connect_5_6 = ic1.strt_bend_strt_p2p(pin1 = insertion_connect5, pin2 = insertion_connect6).put()

#insertion loss test 4
insertion_connect7 = ic1.strt(length=20).put(gc_list[6].pin['a0'])
insertion_connect8 = ic1.strt(length=20).put(gc_list[7].pin['a0'])
insertion_connect_7_8 = ic1.strt_bend_strt_p2p(pin1 = insertion_connect7, pin2 = insertion_connect8).put()

#insertion loss test 5
insertion_connect9 = ic1.strt(length=20).put(gc_list[8].pin['a0'])
insertion_connect10 = ic1.strt(length=20).put(gc_list[9].pin['a0'])
insertion_connect_9_10 = ic1.strt_bend_strt_p2p(pin1 = insertion_connect9, pin2 = insertion_connect10).put()

#placing row 1 single splitters
row1_ini_pos = [230,100]
splitter1 = splitter().put(row1_ini_pos[0]+fiber_pitch,row1_ini_pos[1])
ic1.strt_bend_strt_p2p(pin1 = gc_list2[0].pin['a0'], pin2 = splitter1.pin['a0']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list2[1].pin['a0'], pin2 = splitter1.pin['a1']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list2[2].pin['a0'], pin2 = splitter1.pin['b1']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list2[3].pin['a0'], pin2 = splitter1.pin['b0']).put()

#spliter2 has 7.83um coupling length
splitter2 = splitter(coupling_length=7.83).put(row1_ini_pos[0]+5*fiber_pitch,row1_ini_pos[1])
ic1.strt_bend_strt_p2p(pin1 = gc_list2[4].pin['a0'], pin2 = splitter2.pin['a0']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list2[5].pin['a0'], pin2 = splitter2.pin['a1']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list2[6].pin['a0'], pin2 = splitter2.pin['b1']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list2[7].pin['a0'], pin2 = splitter2.pin['b0']).put()

#placing row 2 elements
row2_ini_pos = [230,350]
row2_splitter1 = []
row2_splitter2 = []
cascade_splitter_count = 4
#placing cascading splitters with 8.17um coupling length
for kk in range(cascade_splitter_count):
    row2_splitter1.append(splitter().put(row2_ini_pos[0]+kk*fiber_pitch,row2_ini_pos[1]))
    ic1.strt_bend_strt_p2p(pin1 = row2_splitter1[kk].pin['b1'],pin2 = gc_list3[kk+1].pin['a0']).put()
    wt.put(row2_splitter1[kk].pin['a1'])
for kk in range (cascade_splitter_count-1):#connecting cascading splitters
    ic1.strt_p2p(pin1 = row2_splitter1[kk],pin2 = row2_splitter1[kk+1].pin['a0']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list3[0].pin['a0'], pin2 = row2_splitter1[0].pin['a0']).put()
wt.put(row2_splitter1[cascade_splitter_count-1].pin['b0'])

#placing cascading splitters with 7.83um coupling length
for kk in range(cascade_splitter_count):#placing splitters and connecting to grating couplers
    row2_splitter2.append(splitter(coupling_length=7.83).put(row2_ini_pos[0]+kk*fiber_pitch+5*fiber_pitch,row2_ini_pos[1]))
    ic1.strt_bend_strt_p2p(pin1 = row2_splitter2[kk].pin['b1'],pin2 = gc_list3[kk+1+5].pin['a0']).put()
    wt.put(row2_splitter2[kk].pin['a1'])
for kk in range (cascade_splitter_count-1):#connecting cascading splitters
    ic1.strt_p2p(pin1 = row2_splitter2[kk],pin2 = row2_splitter2[kk+1].pin['a0']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list3[5].pin['a0'], pin2 = row2_splitter2[0].pin['a0']).put()
wt.put(row2_splitter2[cascade_splitter_count-1].pin['b0'])

#placing row 3 elements
row3_ini_pos = [230,600]
row3_splitter1 = []
row3_splitter2 = []
#placing cascading splitters with 8um coupling length
for kk in range(cascade_splitter_count):
    row3_splitter1.append(splitter(coupling_length=8).put(row3_ini_pos[0]+kk*fiber_pitch,row3_ini_pos[1]))
    ic1.strt_bend_strt_p2p(pin1 = row3_splitter1[kk].pin['b1'],pin2 = gc_list4[kk+1].pin['a0']).put()
    wt.put(row3_splitter1[kk].pin['a1'])
for kk in range (cascade_splitter_count-1):#connecting cascading splitters
    ic1.strt_p2p(pin1 = row3_splitter1[kk],pin2 = row3_splitter1[kk+1].pin['a0']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list4[0].pin['a0'], pin2 = row3_splitter1[0].pin['a0']).put()
wt.put(row3_splitter1[cascade_splitter_count-1].pin['b0'])

#placing cascading splitters with 8.34um coupling length
for kk in range(cascade_splitter_count):#placing splitters and connecting to grating couplers
    row3_splitter2.append(splitter(coupling_length=8.34).put(row3_ini_pos[0]+kk*fiber_pitch+5*fiber_pitch,row3_ini_pos[1]))
    ic1.strt_bend_strt_p2p(pin1 = row3_splitter2[kk].pin['b1'],pin2 = gc_list4[kk+1+5].pin['a0']).put()
    wt.put(row3_splitter2[kk].pin['a1'])
for kk in range (cascade_splitter_count-1):#connecting cascading splitters
    ic1.strt_p2p(pin1 = row3_splitter2[kk],pin2 = row3_splitter2[kk+1].pin['a0']).put()
ic1.strt_bend_strt_p2p(pin1 = gc_list4[5].pin['a0'], pin2 = row3_splitter2[0].pin['a0']).put()
wt.put(row3_splitter2[cascade_splitter_count-1].pin['b0'])


### Part 5: text ###
####################
text_insert1 = str(round(insertion_connect1.length_geo+insertion_connect2.length_geo+insertion_connect_1_2.length_geo,0))+"um"
nd.text(text=text_insert1, height=10, layer=2, align='lb').put(insertion_connect_1_2.bbox[0]-20,(insertion_connect_1_2.bbox[1]+insertion_connect_1_2.bbox[3])/2)
text_insert2 = str(round(insertion_connect3.length_geo+insertion_connect4.length_geo+insertion_connect_3_4.length_geo,0))+"um"
nd.text(text=text_insert2, height=10, layer=2, align='lb').put(insertion_connect_3_4.bbox[0]-20,(insertion_connect_3_4.bbox[1]+insertion_connect_3_4.bbox[3])/2)
text_insert3 = str(round(insertion_connect5.length_geo+insertion_connect6.length_geo+insertion_connect_5_6.length_geo,0))+"um"
nd.text(text=text_insert3, height=10, layer=2, align='lb').put(insertion_connect_5_6.bbox[0]-20,(insertion_connect_5_6.bbox[1]+insertion_connect_5_6.bbox[3])/2)
text_insert4 = str(round(insertion_connect7.length_geo+insertion_connect8.length_geo+insertion_connect_7_8.length_geo,0))+"um"
nd.text(text=text_insert4, height=10, layer=2, align='lb').put(insertion_connect_7_8.bbox[0]-20,(insertion_connect_7_8.bbox[1]+insertion_connect_7_8.bbox[3])/2)
text_insert5 = str(round(insertion_connect9.length_geo+insertion_connect10.length_geo+insertion_connect_9_10.length_geo,0))+"um"
nd.text(text=text_insert5, height=10, layer=2, align='lb').put(insertion_connect_9_10.bbox[0]-20,(insertion_connect_9_10.bbox[1]+insertion_connect_9_10.bbox[3])/2)

nd.text(text="0.12/8.17um", height=10, layer=2, align='lb').put(230+fiber_pitch,50)
nd.text(text="0.12/7.83um", height=10, layer=2, align='lb').put(230+5*fiber_pitch,50)

nd.text(text="0.12/8.17um", height=10, layer=2, align='lb').put(230,300)
nd.text(text="0.12/7.83um", height=10, layer=2, align='lb').put(230+5*fiber_pitch,300)
nd.text(text="0.12/8um", height=10, layer=2, align='lb').put(230,550)
nd.text(text="0.12/8.34um", height=10, layer=2, align='lb').put(230+5*fiber_pitch,550)
### Part XX: export the GDS ###
###############################
nd.export_gds(filename=file_name)




