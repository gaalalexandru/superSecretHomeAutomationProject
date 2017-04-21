#include "stdbool.h"
#include "stdint.h"
#include "ssi_handler_tw.h"

/*-------------------Driver Includes-----------------*/
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/ssi.h"
#include "driverlib/sysctl.h"
#include "inc/hw_memmap.h"
#include "display.h"

#define DIVISOR_rgb 12
#define FREQ_SHIFT_RG 25000000 



void SSI0_DataOut(uint8_t data){ 
	SSIDataPut(SSI0_BASE,data); //Puts a data element into the SSI transmit FIFO.
	Display_NewLine();	
	//Display_String("temp: ");
	Display_Decimal(data); 
}
void SSI1_DataOut(uint8_t data){ 
	SSIDataPut(SSI1_BASE,data); //Puts a data element into the SSI transmit FIFO.
}


void SSI0_InitMaster(void){//for shift register
	uint8_t delay = 0;
	
	SysCtlPeripheralEnable(SYSCTL_PERIPH_SSI0);		//SSI 0 enable 
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);	//Port A enable
	
	SSIDisable(SSI0_BASE);												 //Disable SSI0

	GPIOPinConfigure(GPIO_PA2_SSI0CLK);		//PA2 - Clock
	GPIOPinConfigure(GPIO_PA5_SSI0TX);		//PA5 - TX
	GPIOPinConfigure(GPIO_PA4_SSI0RX);		//PA4 - RX
		GPIOPinConfigure(GPIO_PA3_SSI0FSS);		//PA3 - FSS
	
	GPIOPinTypeSSI(GPIO_PORTA_BASE, GPIO_PIN_2 | GPIO_PIN_3 | GPIO_PIN_5 | GPIO_PIN_4);	// Configure PA2, PA5, PA4 as SSI
	
	SSIClockSourceSet(SSI0_BASE, SSI_CLOCK_SYSTEM);	// Set the SSI clock source

	
	//Peripherial base, Input clock, Frame format(freescale format), Mode, Bit Data Rate,	Data Width	
	SSIConfigSetExpClk(SSI0_BASE, SysCtlClockGet(), SSI_FRF_MOTO_MODE_0, SSI_MODE_MASTER, SysCtlClockGet()/8, 8);
	SSIEnable(SSI0_BASE);				//Enable SSI

  for(delay=0; delay<10; delay=delay+1);// delay minimum 100 ns
}


/*
void SSI1_InitSlave(void)
{
	uint8_t delay = 0;
	SysCtlPeripheralEnable(SYSCTL_PERIPH_SSI1);		//SSI 0 enable 
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);	//Port F enable
	
	SSIDisable(SSI1_BASE);												 //Disable SSI0

	GPIOPinConfigure(GPIO_PF2_SSI1CLK);		//PF2 Clock
	GPIOPinConfigure(GPIO_PF1_SSI1TX);		//PF1 TX
	GPIOPinConfigure(GPIO_PF0_SSI1RX);		//PF0 RX
	GPIOPinConfigure(GPIO_PF3_SSI1FSS); //PF3 FSS 
	GPIOPinTypeSSI(GPIO_PORTF_BASE, GPIO_PIN_2 | GPIO_PIN_1 | GPIO_PIN_0| GPIO_PIN_3);	// Configure PF as SSI
	
	SSIClockSourceSet(SSI1_BASE, SSI_CLOCK_SYSTEM);	// Set the SSI clock source

	
	//Peripherial base, Input clock, Frame format(freescale format), Mode, Bit Data Rate,	Data Width	
	SSIConfigSetExpClk(SSI1_BASE, SysCtlClockGet(), SSI_FRF_MOTO_MODE_0, SSI_MODE_SLAVE, SysCtlClockGet(), 8);	
	SSIEnable(SSI1_BASE);				//Enable SSI
	
	for(delay=0; delay<10; delay=delay+1);// delay minimum 100 ns
}
*/
// Interrupt handler for SSI1 peripheral in slave mode.  It reads the interrupt
// status and if the interrupt is fired by a RX time out interrupt it reads the
// SSI1 RX FIFO and increments a counter to tell the main loop that RX timeout
// interrupt was fired.
/*
void SSI1_IntHandler() //interrupt for slave
{
	unsigned long ulStatus, ulIndex;
	//
	// Read interrupt status.
	//
	ulStatus = SSIIntStatus(SSI1_BASE, 1);
	//
	// Check the reason for the interrupt.
	//
	if(ulStatus & SSI_RXTO)
	{
		//
		// Interrupt is because of RX time out.  So increment counter to tell
		// main loop that RX timeout interrupt occurred.
		//
		g_ulSSI1RXTO++;
		//
		// Read NUM_SSI_DATA bytes of data from SSI1 RX FIFO.
		//
		for(ulIndex = 0; ulIndex < NUM_SSI_DATA; ulIndex++)
		{
			SSIDataGet(SSI1_BASE, &g_ulDataRx1[ulIndex]); // Read NUM_SSI_DATA bytes of data from SSI1 RX FIFO.
		}
	}

	//
	// Clear interrupts.
	//
	SSIIntClear(SSI1_BASE, ulStatus);
}

*/



void SSI1_Init(void){ //for rgb strip
	uint8_t delay = 0;
	
	SysCtlPeripheralEnable(SYSCTL_PERIPH_SSI1);		//SSI 1 enable 
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);	//Port D enable
	
	SSIDisable(SSI1_BASE);												 //Disable SSI1

	GPIOPinConfigure(GPIO_PD0_SSI1CLK);		//PD0 - Clock
	GPIOPinConfigure(GPIO_PD3_SSI1TX);		//PD3 - TX
	GPIOPinTypeSSI(GPIO_PORTD_BASE, GPIO_PIN_0 | GPIO_PIN_3);	// Configure PD0 and PD3 as SSI
	
	SSIClockSourceSet(SSI1_BASE, SSI_CLOCK_SYSTEM);	// Set the SSI clock source

	
	//Peripherial base, Input clock, Frame format(freescale format), Mode, Bit Data Rate,	Data Width	
	SSIConfigSetExpClk(SSI1_BASE, SysCtlClockGet(), SSI_FRF_MOTO_MODE_0, SSI_MODE_MASTER, SysCtlClockGet()/DIVISOR_rgb, 8); //bit data rate for RGB 80MHz/12 = 6666666
	SSIEnable(SSI1_BASE);				//Enable SSI

  for(delay=0; delay<10; delay=delay+1);// delay minimum 100 ns
}
