import numpy as np
import os
# import module
import shutil

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

from wsgiref.validate import PartialIteratorWrapper
from mp0 import VehicleAgent, PedestrianAgent, VehiclePedestrianSensor, verify_refine, eval_velocity, sample_init
from verse import Scenario, ScenarioConfig
from vehicle_controller import VehicleMode, PedestrianMode

from verse.plotter.plotter2D import *
from verse.plotter.plotter3D_new import *
import plotly.graph_objects as go
import copy
import json
import sys
import time

# from pymongo import MongoClient


def grading(netids):
    netid = netids[0]
    script_dir = os.path.realpath(os.path.dirname(__file__))
    input_code_name = os.path.join(script_dir, "vehicle_controller.py")
    vehicle = VehicleAgent('car', file_name=input_code_name)
    pedestrian = PedestrianAgent('pedestrian')

    scenario = Scenario(ScenarioConfig(init_seg_length=1, parallel=False))

    scenario.add_agent(vehicle) 
    scenario.add_agent(pedestrian)
    scenario.set_sensor(VehiclePedestrianSensor())

    init_car_dict = [
        [[-5,-5,0,8],[5,5,0,8]],
        [[-5,-5,0,5],[5,5,0,10]],
        [[-5,-5,0,5],[5,5,0,10]]
    ]

    init_pedestrian_dict = [
        [[175,-55,0,3],[175,-55,0,3]],
        [[175,-55,0,3],[175,-55,0,3]],
        [[165,-55,0,3],[175,-50,0,3]]
    ]

    total_score = 0
    for idx, (init_car, init_pedestrian) in enumerate(zip(init_car_dict, init_pedestrian_dict)):

        scenario.set_init_single(
            'car', init_car,(VehicleMode.Normal,)
        )
        scenario.set_init_single(
            'pedestrian', init_pedestrian, (PedestrianMode.Normal,)
        )

        # # ----------- Simulate multi: Uncomment this block to perform batch of simulations -------------
        if idx == 0 or idx == 1:
            init_dict_list= sample_init(scenario, num_sample=100)
        elif idx == 2:
            init_dict_list= sample_init(scenario, num_sample=100)
            for car_x in [5]:
                for car_y in [-5,-4, 4, 5]:
                    for car_vel in [8, 9, 10]:
                        for ped_x in [165, 166, 167]:
                            for ped_y in [-55]:
                                init_dict_list.append({'car': [car_x, car_y, 0, car_vel], 'pedestrian': [ped_x, ped_y, 0, 3]})
                                
        traces = scenario.simulate_multi(50, 0.1,\
             init_dict_list=init_dict_list)
        fig = go.Figure()
        for trace in traces:
            fig = simulation_tree_3d(trace, fig,\
                                      0,'time', 1,'x',2,'y')
        # fig.show()
        fig.write_image(file=f'log/{netid}.png', format='png')
        fig.write_html(file=f'log/{netid}_R{idx+1}.html')
        avg_vel, unsafe_frac, unsafe_init = eval_velocity(traces)
        # avg_vel = avg_vel[0]
        (avg_vel,) = avg_vel
        print(f"###### Average velocity {avg_vel}, Unsafe fraction {unsafe_frac}, Unsafe init {unsafe_init}")
        # # -----------------------------------------

        if avg_vel == None:
            avg_vel = 0
        penalty = 0.5 if avg_vel <=7 else 0
        if idx == 0:
            score = 10
        elif idx == 1:
            score = 15
        elif idx == 2:
            score = 20
        region_score = score * (1-penalty) * (1-unsafe_frac)
        total_score += region_score
        with open(f'grade.txt', 'a') as f:
            f.write(f"R{idx+1}({score}pts) --  Avg_vel={avg_vel}, unsafe_grac={unsafe_frac}, score={region_score}\n")

        if idx == 2:
            with open(f'grade.txt', 'a') as f:
                f.write(f"Autograded Total Score: {total_score}\n")

        if unsafe_init:
            with open(f'counter-example.txt', 'a') as f:
                f.write(f"R{idx+1}\n")
                f.write(json.dumps(unsafe_init))
                f.write("\n\n")
    
    return region_score, total_score, avg_vel

def main():
    for filename in os.listdir("submission"):
        start_time = time.time()
        netids = filename.split('.py')[0].split("_")
        print("Now grading: ", netids)

        # copy the contents of the demo.py file to  a new file called demo1.py
        shutil.copyfile('submission/{}'.format(filename), './vehicle_controller.py')
        with open('counter-example.txt', 'w') as fp:
            pass

        # block printing of individual testing
        sys.stdout = open(os.devnull, 'w')
        R3_score, total_score, avg_vel = grading(netids)
        sys.stdout = sys.__stdout__

        # Easy for canvas grade uploading
        print("Now Sending Email and clean up")
        with open("class_mp1_score.txt", 'a') as f:
            for netid in netids:
                f.write(f"{netid}, {total_score}\n")
                
        os.system(f"mv grade.txt log/{netids[0]}_grade.txt")
        os.system(f"mv counter-example.txt log/{netids[0]}_counter-example.txt")
        end_time = round(time.time()-start_time, 2)
        print(f"Total Time: {end_time}s\n")

if __name__ == "__main__":
    main()