#TODO re-read
import random
from village.custom_classes.task import BpodEvent, BpodOutput, Task
from BpodPorts import BpodPorts


class S3(Task):

    def __init__(self):
        super().__init__()

        self.info = """
Center-Initiated Side Alternation Task
-----------------------------------------------------------------------------------
Purpose: Introduce penalty for the error
• Structure:
    - Mice initiate each trial by poking the center port (center LED on).
    - After center poke, one side LEDs turn on.
    - Only one side delivers reward (correct side); the other is inactive.
    - Initial side is randomly selected at session start.
• Trial logic:
    - Correct poke → water delivery.
    - Wrong poke → time-out, buzzer noise, and trial termination.
    - After reward or timeup, short delay before next trial.
"""

    def start(self):

        self.trial_count = 0
        self.reward_drunk = 0
        self.iti_time = self.settings.iti_time

        self.ports = BpodPorts(
            water_calibration=self.water_calibration,
            sound_calibration=self.sound_calibration,
            settings=self.settings
        )
        
    def create_trial(self):
        
        self.side = random.choice(["left", "right"])

        # --- mapping ---
        if self.side == "left":
            self.correct_side = "left"
            self.wrong_side   = "right"
            self.correct_poke = self.ports.left_poke
            self.wrong_poke   = self.ports.right_poke
            self.valvetime    = self.ports.valve_l_time
            self.valve_action = self.ports.valve_l_reward
        else:
            self.correct_side = "right"
            self.wrong_side   = "left"
            self.correct_poke = self.ports.right_poke
            self.wrong_poke   = self.ports.left_poke
            self.valvetime    = self.ports.valve_r_time
            self.valve_action = self.ports.valve_r_reward

        print(self.valvetime)
        print(self.valve_action)


        #### CREATING STATE MACHINE, ADDING STATES, SENDING AND RUNNING ####        
        self.bpod.add_state(
            state_name='c_led_on',
            state_timer=self.settings.c_led_on_time,
            state_change_conditions={BpodEvent.Tup: 'exit',
                                    self.ports.center_poke: 'side_led_on'},
            output_actions=[self.ports.LED_c_on]
        )

        self.bpod.add_state(
            state_name='side_led_on',
            state_timer=self.settings.led_on_time,
            state_change_conditions={BpodEvent.Tup: 'exit',
                                    self.correct_poke: 'water_delivery',
                                    self.wrong_poke: 'wrong_choice'},
            output_actions=[self.correct_led]
        )

        self.bpod.add_state(
            state_name='water_delivery',
            state_timer=self.valvetime,
            state_change_conditions={BpodEvent.Tup: 'iti'},
            output_actions=[self.valve_action]
        )

        self.bpod.add_state(
            state_name='iti',
            state_timer=self.iti_time,
            state_change_conditions={Event.Tup: 'exit'},
            output_actions=[]
        )
        
        self.bpod.add_state(
            state_name='wrong_choice',
            state_timer=self.noise_time,
            state_change_conditions={
                BpodEvent.Tup: 'timeout'
            },
            output_actions=[BpodOutput.SoftCode2
            ]
        )

        self.bpod.add_state(
            state_name='timeout',
            state_timer=(self.timeout-self.noise_time), #3s of noise = 10s time-out
            state_change_conditions={
                BpodEvent.Tup: 'exit'
            },
            output_actions=[]
        )


    def after_trial(self):
        # salva il target del trial (lato corretto mostrato)
        self.register_value('rewarded_side', self.side)


        first_poke = self.trial_data.get('STATE_side_led_on_START')
        if first_poke and len(first_poke) > 0 and first_poke[0] > 0:
            water = 0
            outcome = "miss"
            response_side = "none"

            state = self.trial_data.get('STATE_water_delivery_START')
            if state and len(state) > 0 and state[0] > 0:
                water = self.settings.volume
                outcome = "correct"
                response_side = self.correct_side
                
            state = self.trial_data.get('STATE_penalty_START')
            if state and len(state) > 0 and state[0] > 0:
                outcome = "incorrect"
                response_side = self.wrong_side
        else:
            water = 0
            outcome = "omission"
            response_side = "none"


        # registra
        self.register_value('water', water)
        self.register_value('outcome', outcome)
        self.register_value('response_side', response_side)

    def close(self):
        pass
        
        




        
        


