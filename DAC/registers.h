#ifndef REGISTERS_H
#define REGISTERS_H

#include <stdint.h>
#include <stdio.h>
#include "registers.c"

// Register Addresses
#define CONFIGURATION_REGISTER      0x00
#define ANALOG_MONITOR_SELECT       0x01
#define GPIO_REGISTER               0x02
#define OFFSET_DAC_A                0x03
#define OFFSET_DAC_B                0x04
#define RESERVED_REGISTER           0x05
#define SPI_MODE                    0x06
#define BROADCAST_REGISTER          0x07
#define DAC_REGISTER_0              0x08

//Please Add the Register address accordingly

#define ZERO_REGISTER_BASE          0x17
#define GAIN_REGISTER_BASE          0x1F


extern uint32_t create_spi_packet(uint8_t rw, uint8_t address, uint16_t data);

#endif // REGISTERS_H
