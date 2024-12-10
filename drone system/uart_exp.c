#include <ch32v003.h>

void UART_Init(void) {
    // Включаем тактирование USART1
    RCC->APB1ENR |= RCC_APB1ENR_USART1EN; 

    // Настройка скорости передачи
    USART1->BRR = 0x1D4C; // Установка скорости 9600 (для 8MHz)
    USART1->CR1 |= USART_CR1_TE | USART_CR1_RE; // Включаем передатчик и приемник
    USART1->CR1 |= USART_CR1_UE; // Включаем USART
}

char UART_ReadChar(void) {
    while (!(USART1->SR & USART_SR_RXNE)); // Ждем, пока данные не будут готовы к чтению
    return USART1->DR; // Читаем данные из регистра данных
}

void UART_SendChar(char c) {
    while (!(USART1->SR & USART_SR_TXE)); // Ждем, пока передатчик не будет готов
    USART1->DR = c; // Отправляем символ
}

int main(void) {
    UART_Init(); // Инициализация UART

    while (1) {
        char receivedChar = UART_ReadChar(); // Читаем символ из UART
        UART_SendChar(receivedChar); // Отправляем обратно полученный символ (эхо)
    }
}