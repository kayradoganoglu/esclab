import numpy as np
from abstraction import EscData, take_values_from_csv


class PostProcess(EscData):
    def __init__(self, esc_data,type=0,esc_id=0,pole_value=23):
        super().__init__(esc_data.voltage, esc_data.current, esc_data.temp, esc_data.e_rpm, esc_data.t_duty,
                         esc_data.m_duty, esc_data.phase_current, esc_data.pwr, esc_data.stat_1, esc_data.stat_2,esc_data.serial_number)
        self.rpm = self.compute_rpm(pole_value)
        self.running_array=[(1,0,0,0,0,1,0,1,0,1),(0,1,0,0,1,0,1,0,1,1),(0,0,1,0,1,1,0,0,1,1),(0,0,0,1,0,0,1,1,1,0)]
        self.zero_crossing=[]
        self.mean_rpm=[]
        self.mean_thr=[]
        self.mean_voltage=[]
        self.mean_current=[]
        self.mean_temp=[]
        self.mean_phase_current=[]
        self.mean_pwr=[]
        self.mean_m_duty=[]
        self.test_type=type
        if type == 0:
            self.t_duty.insert(0,0)
            self.synchronize_steps(self.detect_step_commands())
            self.crop_data()
        elif type == 1:
            #self.start_end_crop()
            print("type==1","esc_id:",esc_id)
            self.find_zero_crossing()
            print(self.zero_crossing)
            self.combined_step_syncro(esc_id=esc_id)
        elif type == 2:
            self.start_end_crop()
            self.find_zero_crossing_flight()
            print(self.zero_crossing)
            self.flight_syncro()
        else:
            print("Error: Post Process Type Not recognized.")

    def start_end_crop(self):
        # Crop from the start
        for i ,value in enumerate(self.t_duty):
            if value <= 3:
                self.t_duty[i] = 0

        for i, value in enumerate(self.t_duty):
            if value == 0:
                # Crop all lists up to and including the first zero in t_duty
                self.timestamp = self.timestamp[i:]
                self.voltage = self.voltage[i:]
                self.current = self.current[i:]
                self.temp = self.temp[i:]
                self.e_rpm = self.e_rpm[i:]
                self.t_duty = self.t_duty[i:]
                self.m_duty = self.m_duty[i:]
                self.phase_current = self.phase_current[i:]
                self.pwr = self.pwr[i:]
                self.stat_1 = self.stat_1[i:]
                self.stat_2 = self.stat_2[i:]
            else:
                break
        for i in range(len(self.t_duty) - 1, -1, -1):
            if self.t_duty[i] == 0:
                # Crop all lists after the first zero from the end in t_duty
                self.timestamp = self.timestamp[:i + 1]
                self.voltage = self.voltage[:i + 1]
                self.current = self.current[:i + 1]
                self.temp = self.temp[:i + 1]
                self.e_rpm = self.e_rpm[:i + 1]
                self.t_duty = self.t_duty[:i + 1]
                self.m_duty = self.m_duty[:i + 1]
                self.phase_current = self.phase_current[:i + 1]
                self.pwr = self.pwr[:i + 1]
                self.stat_1 = self.stat_1[:i + 1]
                self.stat_2 = self.stat_2[:i + 1]
            else:
                break
            
    def flight_syncro(self, duration_sec=100):
        time = []
        rpm = []
        current = []
        motor_duty = []
        temp = []
        throttle_duty = []
        voltage = []
        phase_cur = []
        pow = []

        num_segments = len(self.zero_crossing)
        if num_segments == 0:
            print("No valid segments found in zero_crossing.")
            return

        segment_duration = duration_sec / num_segments
        current_time = 0

        for (step_start_idx, step_end_idx) in self.zero_crossing:
            num_points = step_end_idx - step_start_idx + 1
            if num_points <= 0:
                continue

            dt = segment_duration / num_points
            t_temp = np.arange(current_time, current_time + segment_duration, dt)

            # Trim t_temp in case rounding causes mismatch
            t_temp = t_temp[:num_points]

            time.extend(t_temp)
            rpm.extend(self.rpm[step_start_idx:step_end_idx + 1])
            current.extend(self.current[step_start_idx:step_end_idx + 1])
            motor_duty.extend(self.m_duty[step_start_idx:step_end_idx + 1])
            temp.extend(self.temp[step_start_idx:step_end_idx + 1])
            throttle_duty.extend(self.t_duty[step_start_idx:step_end_idx + 1])
            voltage.extend(self.voltage[step_start_idx:step_end_idx + 1])
            phase_cur.extend(self.phase_current[step_start_idx:step_end_idx + 1])
            pow.extend(self.pwr[step_start_idx:step_end_idx + 1])

            current_time += segment_duration

        # Atama
        self.timestamp = time
        self.rpm = rpm
        self.current = current
        self.m_duty = motor_duty
        self.temp = temp
        self.t_duty = throttle_duty
        self.voltage = voltage
        self.phase_current = phase_cur
        self.pwr = pow

        print(f"🛫 Flight sync complete: {len(time)} timestamps across {num_segments} segments.")


    def find_zero_crossing_flight(self):
        self.zero_crossing = []
        start_index = None

        for i in range(1, len(self.timestamp)):
            if self.t_duty[i - 1] == 0 and self.t_duty[i] != 0:
                start_index = i
            elif self.t_duty[i - 1] != 0 and self.t_duty[i] == 0 and start_index is not None:
                end_index = i
                self.zero_crossing.append((start_index, end_index))
                start_index = None


    def combined_step_syncro(self, esc_id, step_duration_sec=35):
        time, rpm, current, motor_duty, temp, throttle_duty, voltage = [], [], [], [], [], [], []
        phase_cur , pow = [],[]
        running_arr = self.running_array[esc_id]

        total_duration_sec = step_duration_sec * len(running_arr)

        overall_dt = total_duration_sec / len(running_arr)

        current_time = 0
        j=0
        for i_stp, run in enumerate(running_arr):
            if run:  # Only process steps where the ESC is running
                (step_start_idx, step_end_idx) = self.zero_crossing[j]
                j+=1
                num_points = step_end_idx - step_start_idx + 1

                dt = step_duration_sec / num_points

                t_temp = np.arange(i_stp * step_duration_sec, (i_stp + 1) * step_duration_sec, dt)
                time.extend(t_temp)
                rpm.extend(self.rpm[step_start_idx:step_end_idx + 1])
                current.extend(self.current[step_start_idx:step_end_idx + 1])
                motor_duty.extend(self.m_duty[step_start_idx:step_end_idx + 1])
                temp.extend(self.temp[step_start_idx:step_end_idx + 1])
                throttle_duty.extend(self.t_duty[step_start_idx:step_end_idx + 1])
                voltage.extend(self.voltage[step_start_idx:step_end_idx + 1])
                phase_cur.extend(self.phase_current[step_start_idx:step_end_idx + 1])
                pow.extend(self.pwr[step_start_idx:step_end_idx + 1])

            j = 0
            current_time += step_duration_sec
            time.append(current_time)
            rpm.append(0)
            current.append(0)
            motor_duty.append(0)
            temp.append(0)
            throttle_duty.append(0)
            voltage.append(0)
            phase_cur.append(0)
            pow.append(0)

        if not running_arr[-1]:
            num_points = len(time) - len(rpm)
            print("NumPoints",num_points)
            if num_points > 0:
                t_temp = np.linspace(current_time, current_time + step_duration_sec, num_points, endpoint=False)
                time.extend(t_temp)

        if len(time) != len(rpm):
            raise ValueError("Mismatch in the length of time and data arrays")

        self.rpm = rpm
        self.current = current
        self.m_duty = motor_duty
        self.temp = temp
        self.t_duty = throttle_duty
        self.voltage = voltage
        self.timestamp = time
        self.phase_current = phase_cur
        self.pwr=pow

        print(f"Final timestamp: {self.timestamp[-1]} seconds, Length {len(self.timestamp)}")

    def find_zero_crossing(self):
        start_index = []
        end_index = []

        for i in range(1, len(self.timestamp)):
            if self.t_duty[i] == 0 and self.t_duty[i - 1] != 0:
                start_index.append(self.timestamp[i])
            elif self.t_duty[i] != 0 and self.t_duty[i - 1] == 0:
                end_index.append(self.timestamp[i])

        for i in (range(len(end_index))):
            self.zero_crossing.append((end_index[i], start_index[i+1]))

    def compute_rpm(self,var=23):
        return np.array(self.e_rpm) / var

    def crop_data(self):
        del self.voltage[len(self.timestamp)-1:]
        del self.current[len(self.timestamp)-1:]
        del self.temp[len(self.timestamp)-1:]
        del self.rpm[len(self.timestamp)-1:]
        del self.t_duty[len(self.timestamp)-1:]
        del self.m_duty[len(self.timestamp)-1:]
        del self.phase_current[len(self.timestamp)-1:]
        del self.pwr[len(self.timestamp)-1:]
        del self.stat_1[len(self.timestamp)-1:]
        del self.stat_2[len(self.timestamp)-1:]
        del self.timestamp[-1]

    def detect_step_commands(self, threshold=9, min_gap=5):
        step_cmd_diff = np.diff(self.t_duty)
        step_cmd_idx = np.where(np.abs(step_cmd_diff) > threshold)[0]

        step_cmd_idx = [step_cmd_idx[i] for i in range(len(step_cmd_idx))
                        if i == 0 or (step_cmd_idx[i] - step_cmd_idx[i - 1] >= min_gap)]

        return step_cmd_idx

    def detect_difference_pairs(self, pairs: list, threshold_factor: float = 2) -> list:
        if not isinstance(pairs, list) or not all(isinstance(pair, tuple) and len(pair) == 2 for pair in pairs):
            raise TypeError("pairs must be a list of 2-element tuples.")
        differences = [abs(pair[0] - pair[1]) for pair in pairs]
        mean_diff = np.mean(differences)
        std_diff = np.std(differences)

        threshold = mean_diff + threshold_factor * std_diff
        filtered_pairs = [pairs[idx] for idx, diff in enumerate(differences) if diff <= threshold]

        while len(filtered_pairs) > 29:
            filtered_pairs.pop()

        return filtered_pairs

    def synchronize_steps(self, step_cmd_idx, step_duration_sec=5):
        time, rpm, current, motor_duty, temp, throttle_duty, voltage = [], [], [], [], [], [], []
        phase_cur,pow=[],[]
        steps = [(step_cmd_idx[i], step_cmd_idx[i + 1] - 1) for i in range(len(step_cmd_idx) - 1)]

        filtered_steps = self.detect_difference_pairs(steps)

        for i_stp in range(len(filtered_steps)):
            step_start_idx, step_end_idx = filtered_steps[i_stp]

            dt = step_duration_sec / (step_end_idx - step_start_idx + 1)

            t_temp = np.arange(i_stp * step_duration_sec, (i_stp + 1) * step_duration_sec, dt)
            time.extend(t_temp)

            rpm.extend(self.rpm[step_start_idx:step_end_idx + 1])
            current.extend(self.current[step_start_idx:step_end_idx + 1])
            motor_duty.extend(self.m_duty[step_start_idx:step_end_idx + 1])
            temp.extend(self.temp[step_start_idx:step_end_idx + 1])
            throttle_duty.extend(self.t_duty[step_start_idx:step_end_idx + 1])
            voltage.extend(self.voltage[step_start_idx:step_end_idx + 1])
            phase_cur.extend(self.phase_current[step_start_idx:step_end_idx + 1])
            pow.extend(self.pwr[step_start_idx:step_end_idx + 1])

        self.rpm = rpm
        self.current = current
        self.m_duty = motor_duty
        self.temp = temp
        self.t_duty = throttle_duty
        self.voltage = voltage
        self.timestamp = time
        self.phase_current = phase_cur
        self.pwr = pow

        for i_stp in range(len(filtered_steps)):
            step_start_idx, step_end_idx = filtered_steps[i_stp]
            self.mean_rpm.append(np.mean(self.rpm[step_start_idx:step_end_idx + 1]))
            self.mean_thr.append(np.mean(self.t_duty[step_start_idx:step_end_idx + 1]))
            self.mean_voltage.append(np.mean(self.voltage[step_start_idx:step_end_idx + 1]))
            self.mean_current.append(np.mean(self.current[step_start_idx:step_end_idx + 1]))
            self.mean_temp.append(np.mean(self.temp[step_start_idx:step_end_idx + 1]))
            self.mean_phase_current.append(np.mean(self.phase_current[step_start_idx:step_end_idx + 1]))
            self.mean_m_duty.append(np.mean(self.m_duty[step_start_idx:step_end_idx + 1]))

        print("Step Test Values Set.")
