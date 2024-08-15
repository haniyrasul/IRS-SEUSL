#ifndef SPI_INTERFACE_H
#define SPI_INTERFACE_H

#include <stdint.h>
#include "registers.h"
#include "spi_interface.c"


extern void spi_init(void);
extern void spi_send(uint32_t data);
extern uint32_t spi_receive(void);
extern void spi_write_register(uint8_t address, uint16_t data);
extern uint16_t spi_read_register(uint8_t address);

#endif // SPI_INTERFACE_H
