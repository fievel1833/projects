"""This demo UAV is based on a STANAG 4586 communication framework."""
class Aircraft:
    def __init__(self, altitude, pitch, roll, yaw):
        self.altitude = altitude
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
    
    @altitude.setter
    def altitude(self, altitude):
        self.altitude = altitude
        
    @property    
    def altitude(self):
        return self.altitude
    
    @pitch.setter
    def pitch(self, pitch):
        self.pitch = pitch
        
    @property
    def pitch(self):
        return self.pitch
    
    @roll.setter
    def roll(self, roll):
        self.roll = roll
        
    @property
    def roll(self):
        return self.roll
    
    @yaw.setter
    def yaw(self, yaw):
        self.yaw = yaw
    
    @property
    def yaw(self):
        return self.yaw