#include "spi_interface.h"



//
void spi_init(void) {
    // Initialize SPI interface (depends on the microcontroller)
}

void spi_send(uint32_t data) {
    // Send 24-bit data via SPI (depends on the microcontroller)
}
//
uint32_t spi_receive(void) {
    // Receive 24-bit data via SPI (depends on the microcontroller)
    return 0; // Placeholder return value
}

void spi_write_register(uint8_t address, uint16_t data) {
    uint32_t packet = create_spi_packet(1, address, data); // Write 
    spi_send(packet);
}

uint16_t spi_read_register(uint8_t address) {
    uint32_t packet = create_spi_packet(0, address, 0); // Read 
    spi_send(packet);
    return (uint16_t)(spi_receive() & 0x3FFF); // Extract 14-bit data from received packet
}
