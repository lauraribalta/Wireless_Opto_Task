from village.custom_classes.task import Event, Output

class BpodPorts:
    __slots__ = (
        "valve_l_time",
        "valve_l_reward",
        "valve_c_time",
        "valve_c_reward",
        "valve_r_time",
        "valve_r_reward",
        "LED_l_on",
        "LED_c_on",
        "LED_r_on",
        "left_poke",
        "center_poke",
        "right_poke",
        "left_poke_out",
        "center_poke_out",
        "right_poke_out",
        "sound_gain"
    )

    def __init__(self, water_calibration, sound_calibration, settings):

        self.sound_gain= sound_calibration.get_sound_gain(0, 70, "whitenoise")

        self.valve_l_time = water_calibration.get_valve_time(port = 1, volume = settings.volume)
        self.valve_l_reward = Output.Valve1
        
        self.valve_c_time = water_calibration.get_valve_time(port = 2, volume = settings.volume)
        self.valve_c_reward = Output.Valve2

        self.valve_r_time = water_calibration.get_valve_time(port = 3, volume = settings.volume)
        self.valve_r_reward = Output.Valve3

        self.LED_l_on = (Output.PWM1, settings.led_intensity)
        self.LED_c_on = (Output.PWM2, settings.led_intensity)
        self.LED_r_on = (Output.PWM3, settings.led_intensity)

        self.left_poke = Event.Port1In 
        self.center_poke = Event.Port2In
        self.right_poke = Event.Port3In 

        self.left_poke_out = Event.Port1Out 
        self.center_poke_out = Event.Port2Out 
        self.right_poke_out = Event.Port3Out

