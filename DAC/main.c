#include <stdio.h>
#include "spi_interface.h"
#include "registers.h"



int main() {
    

	spi_init();
    
    // Example 1 :  writing to a register
	uint8_t write_address = 0x08; 
    uint16_t write_data = 0x1234;
    spi_write_register(write_address, write_data);

    // Example 2: reading from a register
    uint8_t read_address = 0x06; 
    uint16_t read_data = spi_read_register(read_address);
    printf("Read Data: 0x%04X\n", read_data);


     // Example 3: reading from a register
    uint8_t read_address1 = SPI_MODE; 
    uint16_t read_data1 = spi_read_register(read_address1);
    printf("Read Data: 0x%04X\n", read_data1);

    return 0;
}
