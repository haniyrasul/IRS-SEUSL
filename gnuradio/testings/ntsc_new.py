#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: Rasul
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import Qt
import sip
from gnuradio import fosphor
from gnuradio.fft import window
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network



class ntsc_new(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ntsc_new")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samples_per_line = samples_per_line = 772
        self.center_freq = center_freq = 512000000+1250000
        self.tx_freq = tx_freq = center_freq
        self.samp_rate = samp_rate = samples_per_line * 60 * .999 * 525 / 2
        self.rf_gain = rf_gain = 14
        self.if_gain = if_gain = 40
        self.digital_gain = digital_gain = 0.9
        self.delay = delay = 0
        self.audio_rate = audio_rate = int(48000)

        ##################################################
        # Blocks
        ##################################################

        self._delay_range = qtgui.Range(0, 240e3, 10, 0, 200)
        self._delay_win = qtgui.RangeWidget(self._delay_range, self.set_delay, "Audio Delay", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._delay_win)
        self._tx_freq_range = qtgui.Range(100e6, 700e6, 10e6, center_freq, 200)
        self._tx_freq_win = qtgui.RangeWidget(self._tx_freq_range, self.set_tx_freq, "TX Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_freq_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_gr_complex, 1, '127.0.0.1', 8800, 0, 1472, False)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, [1], (-4.5e6), 12.15e6)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(window.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(center_freq, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._fosphor_qt_sink_c_0_win)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('D:\\University\\Research\\IRS\\Video TxRx\\audio\\minions.mp4', True)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(110e-3)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, 'D:\\University\\Research\\IRS\\Video TxRx\\testing.dat', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 0)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.band_pass_filter_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                samp_rate,
                (-2475000 + 1725000),
                4e6,
                500000,
                window.WIN_HAMMING,
                6.76))
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=48000,
        	quad_rate=480000,
        	tau=(75e-6),
        	max_dev=75e3,
        	fh=(-1.0),
        )
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ntsc_new")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samples_per_line(self):
        return self.samples_per_line

    def set_samples_per_line(self, samples_per_line):
        self.samples_per_line = samples_per_line
        self.set_samp_rate(self.samples_per_line * 60 * .999 * 525 / 2)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_tx_freq(self.center_freq)
        self.fosphor_qt_sink_c_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, (-2475000 + 1725000), 4e6, 500000, window.WIN_HAMMING, 6.76))
        self.fosphor_qt_sink_c_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain

    def get_digital_gain(self):
        return self.digital_gain

    def set_digital_gain(self, digital_gain):
        self.digital_gain = digital_gain

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate




def main(top_block_cls=ntsc_new, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
