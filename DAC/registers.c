#include "registers.h"
#include <stdint.h>

uint32_t create_spi_packet(uint8_t rw, uint8_t address, uint16_t data) {
    
	uint32_t packet = 0;
    rw &= 0x01;        
    address &= 0x1F;   // Address is 5 bits
    data &= 0x3FFF;    // Data is 14 bits

    // Assemble the packet
    packet |= (rw << 23);          
    packet |= (address << 16);     
    packet |= (data << 2);    
	
	printf("SPI Packer\t: 0x%06X\n",packet);     

    return packet;
}
