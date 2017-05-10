/*--------------------Type Includes------------------*/
#include "stdbool.h"
#include "stdint.h"
#include "custom_types.h"

/*--------------------Project Includes------------------*/
#include "startup_container.h"
#include "timer_handler.h"
#include "adc_handler.h"
#include "i2c_handler.h"
#include "gpio_handler.h"  
#include "light_app.h"
#include "pwm_handler.h"  
#include "spi_handler.h"
#include "display.h"

/*-------------------Driverlib Includes-----------------*/
#include "driverlib/interrupt.h"
#include "driverlib/gpio.h" 
#include "driverlib/timer.h"

/*-------------------HW define Includes--------------*/
#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"

extern CommandStruct SlaveCommands[256];
extern uint8_t SlaveResults[256];

void Init_Commands()
{
	
	//SlaveCommands[10].function=&RedOn;
	//SlaveCommands[11].function=&GreenOn;
	//SlaveCommands[12].function=&BlueOn;
	//SlaveCommands[20].function=&RedOff;
	//SlaveCommands[21].function=&GreenOff;
	//SlaveCommands[22].function=&BlueOff;
		SlaveCommands[20].function=&SetL1Red;
		SlaveCommands[21].function=&SetL1Green;
		SlaveCommands[22].function=&SetL1Blue;
		SlaveCommands[23].function=&SetL2Red;
		SlaveCommands[24].function=&SetL2Green;
		SlaveCommands[25].function=&SetL2Blue;
		SlaveCommands[26].function=&SetL3Red;
		SlaveCommands[27].function=&SetL3Green;
		SlaveCommands[28].function=&SetL3Blue;
	
		SlaveCommands[15].function=&Vent1;
		SlaveCommands[16].function=&Vent2;
}

void Init_Results()
{
	uint16_t i = 0;
	for (i = 0; i <=255; i++) {
		SlaveResults[i] = i;  //Fill in global variable for slave results with dummy values
	}
}

void Init_Drivers(void)
{ 
	uint8_t period;
	uint8_t calc;
	Display_Init();
	Display_String("UART0 Initialized");
	I2C_Init(I2C0_BASE,1);
	I2C_Init_LuminositySensor(0x49);
	I2C_Init_LuminositySensor(0x39);
	I2C_Init(I2C1_BASE,0);
	
	Add_ADC_Channel(0);//channel 0
	Add_ADC_Channel(1);//channel 1
	ADC_Init();
	
	
	//SetGPIOInterrupt(GPIO_PORTF_BASE,GPIO_PIN_4,GPIO_RISING_EDGE);
	//debouncing pf4
	//Init_Timer(TIMER4_BASE, TIMER_A,1000);
	
	//SetGPIOInput(GPIO_PORTF_BASE,GPIO_PIN_0,1);
	//SetGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1);//proba pentru verificat ca merge spi commands
	SetGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3);
	 
	SetGPIOOutput(GPIO_PORTB_BASE,GPIO_PIN_6);
	SetGPIOOutput(GPIO_PORTB_BASE,GPIO_PIN_7);
	period = 20; //ventilator
	calc = SysCtlClockGet()/ (1000 * period) - 1;
	Init_PWM(GPIO_PORTB_BASE,GPIO_PIN_6, calc);
		Init_PWM(GPIO_PORTB_BASE,GPIO_PIN_7, calc);


	SSI0_InitSlave();
	Display_String("SPI0 Slave Initialized");
	Init_Commands();
	Init_Results();
	
	//Cyclic 50 ms
	Init_Timer(TIMER0_BASE, TIMER_A,50); 
	TimerEnable(TIMER0_BASE, TIMER_A);
	Display_String("Timer cyclic 50ms initialized");
	
	//Cyclic 100 ms
	Init_Timer(TIMER1_BASE, TIMER_A,100);  
	TimerEnable(TIMER1_BASE, TIMER_A); 	
	Display_String("Timer cyclic 100ms initialized");
	//Cyclic 500 ms
	Init_Timer(TIMER2_BASE, TIMER_A,500);  
	TimerEnable(TIMER2_BASE, TIMER_A); 
	Display_String("Timer cyclic 500ms initialized");
	//Cyclic 1000 ms
	Init_Timer(TIMER3_BASE, TIMER_A,1000);  
	TimerEnable(TIMER3_BASE, TIMER_A); 
	Display_String("Timer cyclic 1000ms initialized");

	SSI1_Init_RGB();
	Display_String("SPI1 Master Initialized for WS2812 LEDs");
	IntMasterEnable();
}
