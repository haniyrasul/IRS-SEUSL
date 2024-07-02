#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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
from gnuradio import dtv
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time



class atsc_tx(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "atsc_tx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 4500000.0 / 286 * 684
        self.pilot_freq = pilot_freq = 309441
        self.center = center = 195e6

        ##################################################
        # Blocks
        ##################################################

        self._center_range = qtgui.Range(88e6, 700e6, 1e6, 195e6, 200)
        self._center_win = qtgui.RangeWidget(self._center_range, self.set_center, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._center_win)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(symbol_rate)
        self.osmosdr_sink_0.set_center_freq(center, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(window.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(474e6, 48000)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._fosphor_qt_sink_c_0_win)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, firdes.root_raised_cosine(0.1, symbol_rate, symbol_rate/2, 0.1152, 100), 2)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.dtv_dvbs2_modulator_bc_0 = dtv.dvbs2_modulator_bc(
            dtv.FECFRAME_NORMAL,
            dtv.C1_4,
            dtv.MOD_8VSB,
            dtv.INTERPOLATION_OFF)
        self.dtv_atsc_trellis_encoder_0 = dtv.atsc_trellis_encoder()
        self.dtv_atsc_rs_encoder_0 = dtv.atsc_rs_encoder()
        self.dtv_atsc_randomizer_0 = dtv.atsc_randomizer()
        self.dtv_atsc_pad_0 = dtv.atsc_pad()
        self.dtv_atsc_interleaver_0 = dtv.atsc_interleaver()
        self.dtv_atsc_field_sync_mux_0 = dtv.atsc_field_sync_mux()
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_char*1, 1024)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_char, 832, 1024, 4)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'D:\\University\\Research\\IRS\\Video TxRx\\new_ts.ts', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.analog_sig_source_x_0 = analog.sig_source_c(symbol_rate, analog.GR_COS_WAVE, (-3000000+pilot_freq), (900e-3), 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.dtv_atsc_pad_0, 0))
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.dtv_dvbs2_modulator_bc_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_keep_m_in_n_0, 0))
        self.connect((self.dtv_atsc_field_sync_mux_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.dtv_atsc_interleaver_0, 0), (self.dtv_atsc_trellis_encoder_0, 0))
        self.connect((self.dtv_atsc_pad_0, 0), (self.dtv_atsc_randomizer_0, 0))
        self.connect((self.dtv_atsc_randomizer_0, 0), (self.dtv_atsc_rs_encoder_0, 0))
        self.connect((self.dtv_atsc_rs_encoder_0, 0), (self.dtv_atsc_interleaver_0, 0))
        self.connect((self.dtv_atsc_trellis_encoder_0, 0), (self.dtv_atsc_field_sync_mux_0, 0))
        self.connect((self.dtv_dvbs2_modulator_bc_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.osmosdr_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "atsc_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.symbol_rate)
        self.fft_filter_xxx_0.set_taps(firdes.root_raised_cosine(0.1, self.symbol_rate, self.symbol_rate/2, 0.1152, 100))
        self.osmosdr_sink_0.set_sample_rate(self.symbol_rate)

    def get_pilot_freq(self):
        return self.pilot_freq

    def set_pilot_freq(self, pilot_freq):
        self.pilot_freq = pilot_freq
        self.analog_sig_source_x_0.set_frequency((-3000000+self.pilot_freq))

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center
        self.osmosdr_sink_0.set_center_freq(self.center, 0)




def main(top_block_cls=atsc_tx, options=None):

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
