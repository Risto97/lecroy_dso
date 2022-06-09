# import pyvisa
import usbtmc
import time
import inspect
import vxi11


class Lecroy:
    def __init__(self, usbtmc=False, lxi=True, IP="0.0.0.0"):

        if lxi == True:
            self.l = vxi11.Instrument(f"TCPIP::{IP}::INSTR")

        elif usbtmc == True:
            rm = usbtmc.list_devices()
            self.l = usbtmc.Instrument(rm[0])
            self.l.timeout = 5000


    def write(self, command):
        self.l.write(f"""vbs '{command}' """)

    def query(self, command):
        return self.l.ask(f"""vbs? '{command}' """).strip()

    """ Trigger """
    """ mode = [auto, normal, single, stopped] """
    def set_trigger_mode(self, value):
        _VALUES = ["auto", "normal", "single", "stopped"]
        assert value in _VALUES, f'In method {inspect.currentframe().f_code.co_name}() value: {value}" not allowed\nAllowed values are: {_VALUES}'

        self.write(f'app.acquisition.triggermode = "{value}"')

    def set_trigger_level(self, level):
        
        self.write(f'app.acquisition.trigger.edge.level = {level}')

    """ Horizontal """
    def set_horizontal_maximize(self, value):
        _VALUES = ["setmaximummemory", "fixedsamplerate"]
        assert value in _VALUES, f'In method {inspect.currentframe().f_code.co_name}() value: {value}" not allowed\nAllowed values are: {_VALUES}'
        self.write(f'app.acquisition.horizontal.maximize = "{value}"')

    def set_horizontal_scale(self, value):
        self.write(f'app.acquisition.horizontal.horscale = "{value}"')

    def set_sample_rate(self, value):
        self.write(f'app.acquisition.horizontal.samplerate = "{value}"')

    def clear_all_measurements(self):
        self.write('app.measure.clearall')
        self.write('app.measure.clearsweeps')

    """ SETUP """
    def auto_setup(self):
        self.write('app.autosetup')

    def set_to_default(self):
        self.write('app.settodefaultsetup')

    def wait_until_idle(self, delay):
        return self.query(f'return=app.WaitUntilIdle({delay})')

    """ VERTICAL """

    def set_vertical_scale(self, channel, scale):
        _CHANNELS = ["C1", "C2", "C3", "C4"]
        assert channel in _CHANNELS, f'In method {inspect.currentframe().f_code.co_name}() channel: {channel}" not allowed\nAllowed channels are: {_CHANNELS}'
        assert (scale >= 0.01 and scale <= 100) , f'In method {inspect.currentframe().f_code.co_name}() scale: {scale}" not allowed\nAllowed values are: [0.01 - 100]'

        self.write(f'app.acquisition.{channel}.verscale = "{scale}"')


    """ MEASURE """
    def set_show_measure(self, value):
        assert type(value) == bool, f'In method {inspect.currentframe().f_code.co_name}() value: {value} not allowed\n Value needs to be bool'

        self.write(f'app.measure.showmeasure = {value}')

    def set_stats_on(self, value):
        assert type(value) == bool, f'In method {inspect.currentframe().f_code.co_name}() value: {value} not allowed\n Value needs to be bool'

        self.write(f'app.measure.statson = {value}')

    def set_measure_view(self, channel, value):
        _CHANNELS = ["C1", "C2", "C3", "C4"]
        assert type(value) == bool, f'In method {inspect.currentframe().f_code.co_name}() value: {value} not allowed\n Value needs to be bool'
        assert channel in _CHANNELS, f'In method {inspect.currentframe().f_code.co_name}() channel: {channel}" not allowed\nAllowed channels are: {_VALUES}'

        self.write(f'app.measure.{channel}.view = {value}')

    def set_measure_param(self, param, value):
        _PARAMS = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
        assert param in _PARAMS, f'In method {inspect.currentframe().f_code.co_name}() param: {param}" not allowed\nAllowed channels are: {_PARAMS}'

        _VALUES = ["100BTfall", "100BTrise", "100BTTIE", "100BTTj", "10BTH", "10BTJ", "Amplitude", "AmplitudeAsymmetry", "Analog2Protocol", \
            "ApparentPower", "Area", "AutoCorrelationSignalTo", "Base", "BurstWidth", "CANLoad", "CANMsgBR", "CANMsgNum", "CANtoAnalog", \
            "CANtoCAN", "CANtoValue", "Cycles", "Delay", "DeltaDelay", "DeltaMessages", "DeltaPeriodAtLevel", "DeltaTimeAtLevel", "DeltaTriggerTime",\
            "DeltaWidthAtLevel", "DOV", "Duration", "DutyAtLevel", "DutyCycle", "DutyCycleDistortion", "EdgeAtLevel", "EMClvlPulse", "EMCt2Val", \
            "EOvshN", "EOvshP", "ExcelParam", "ExtinctionRatio", "EyeAmplitude", "EyeAvgPower", "EyeBER", "EyeCrossing", "EyeHeight", "EyeOneLevel", \
            "EyeQFactor", "EyeWidth", "EyeZeroLevel", "Fall", "Fall8020", "FallAtLevel", "FastMultiWPort", "FirstPoint", "Frequency", "FrequencyAtLevel", "FullWidthAtHalfMaximum", \
            "FullWidthAtXX", "GapWidth", "GBM1FGDroop", "GBM1HJDroop", "HalfPeriod", "HistogramAmplitude", "HistogramBase", "HistogramMaximum", "HistogramMean", "HistogramMedian", \
            "HistogramMid", "HistogramMinimum", "HistogramRms", "HistogramSdev", "HistogramTop", "HoldTime", "HParamScript", "I2StoValue", "LastPoint", "LevelAtX", "LocalBase", \
            "LocalBaselineSeparation", "LocalMaximum", "LocalMinimum", "LocalNumber", "LocalPeakToPeak", "LocalTimeAtMaximum", "LocalTimeAtMinimum", "LocalTimeBetweenEvent", \
            "LocalTimeBetweenPeaks", "LocalTimeBetweenTroug", "LocalTimeOverThreshold", "LocalTimePeakToTrough", "LocalTimeTroughToPeak", "LocalTimeUnderThreshol", "MathcadParam", \
            "MATLABParameter", "Maximum", "MaximumPopulation", "Mean", "Median", "Minimum", "Mode", "NarrowBandPhase", "NarrowBandPower", "NCycleJitter", \
            "NonLinearTransitionShift", "npoints", "Null", "NumberOfModes", "OvershootNegative", "OvershootPositive", "Overwrite", "ParamScript", "PEAKMAG", "Peaks", \
            "PeakToPeak", "Percentile", "Period", "PeriodAtLevel", "Phase", "PopulationAtX", "PowerFactor", "Protocol2Analog", "Protocol2Protocol", "Protocol2Value", \
            "ProtocolBitrate", "ProtocolLoad", "ProtocolNumMessages", "PW50", "PW50Negative", "PW50Positive", "Range", "RealPower", "Resolution", "Rise", \
            "Rise2080", "RiseAtLevel", "RootMeanSquare", "SAS", "Setup", "Skew", "Slew", "StandardDeviation", "TAA", "TAANegative", "TAAPositive", "TIE", "TimeAtCAN", \
            "TimeAtLevel", "TimeAtProtocol", "Top", "TotalPopulation", "tUpS", "Width", "WidthAtLevel", "WidthNegative", "XAtMaximum", "XAtMinimum", "XAtPeak"]
        assert value in _VALUES, f'In method {inspect.currentframe().f_code.co_name}() value: {value}" not allowed\nAllowed values are: {_VALUES}'

        self.write(f'app.measure.{param}.paramengine = "{value}"')

    def set_measure_source(self, param, source1, source2=None):
        _CHANNELS = ["C1", "C2", "C3", "C4"]
        _PARAMS = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
        assert param in _PARAMS, f'In method {inspect.currentframe().f_code.co_name}() param: {param}" not allowed\nAllowed channels are: {_PARAMS}'
        assert source1 in _CHANNELS, f'In method {inspect.currentframe().f_code.co_name}() channel: {source1}" not allowed\nAllowed channels are: {_CHANNELS}'
        _CHANNELS.append(None)
        assert source2 in _CHANNELS, f'In method {inspect.currentframe().f_code.co_name}() channel: {source2}" not allowed\nAllowed channels are: {_CHANNELS}'

        self.write(f'app.measure.{param}.source1 = "{source1}"')

        if source2 != None:
            self.write(f'app.measure.{param}.source2 = "{source2}"')


    """ Acquisition """

    def acquire(self, num):
        for i in range(0, num):
            ret = self.query('return=app.acquisition.acquire( 0.1 , True )')
            r = self.wait_until_idle(5)
            if r == 0:
                print("Time out from WaitUntilIdle, return = {ret}")

    def get_measure_result(self, param):
        _PARAMS = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
        assert param in _PARAMS, f'In method {inspect.currentframe().f_code.co_name}() param: {param}" not allowed\nAllowed channels are: {_PARAMS}'

        ret = self.query(f'return=app.measure.{param}.out.result.value')
        unit = self.query(f'return=app.measure.{param}.out.result.verticalunits')
        return [ret, unit]

    def get_measurement(self, param, paramengine, source1, source2=None):
        self.set_measure_param(param, paramengine)
        self.set_measure_source(param, source1, source2)
        self.acquire(1)
        return self.get_measure_result(param)

# fs w/ lecroy = Lecroy()
#
# lecroy = Lecroy()
# print(lecroy.l.ask("*IDN?"))
#
# lecroy.l.write("COMM_HEADER OFF")
#
# lecroy.set_to_default()
#
# print(lecroy.query('return=app.WaitUntilIdle(5)'))
# #
# lecroy.set_trigger_mode("stopped")
# lecroy.set_trigger_level(0.5)
# lecroy.set_trigger_mode("auto")
# lecroy.set_horizontal_maximize("fixedsamplerate")
#
# lecroy.clear_all_measurements()
#
# lecroy.set_sample_rate(100e3)
# lecroy.set_horizontal_scale("1ms")
#
# lecroy.set_vertical_scale("C1", 0.5)
#
# lecroy.set_show_measure(True)
#
# lecroy.set_measure_param("P1", "Period")
# lecroy.set_measure_source("P1", "C1")
#
# # freq = lecroy.get_measurement("P1", "Frequency", "C1")
# start_time = time.time()
# lecroy.acquire(1)
# freq = lecroy.get_measure_result("P1")
# print("--- %s seconds ---" % (time.time() - start_time))
# # ampl = lecroy.get_measurement("P2", "Amplitude", "C1")
# # rise = lecroy.get_measurement("P3", "Rise", "C1")
#
# print(freq)
# # print(freq, ampl, rise)
#
