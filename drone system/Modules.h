#define Val_Int 10
// Класс DisplayManager

class MyPrint {
public:


    static void printSerial(const String &params) {
        if(params.startsWith("\"") && params.endsWith("\"")) {
            Serial.print(params.substring(1, params.length() - 1));
        } else {
            Serial.print(params);
        }
    }

    static void printlnSerial(const String &params) {
        if (params.startsWith("\"") && params.endsWith("\"")) {
            Serial.println(params.substring(1, params.length() - 1));
        } else {
            Serial.println(params);
        }
    }

    
};

// Инициализация дисплея

// Класс Pin
class Pin {
public:
    static void init(const String &params) {
        int dot = params.indexOf(',');
        String pinStr = params.substring(0, dot);
        String mode = params.substring(dot + 2);
        int pin = pinStr.toInt();
        if (mode == "input") {
            pinMode(pin, INPUT);
        } else if (mode == "output") {
            pinMode(pin, OUTPUT);
        }
    }

    static void read(const String &params) {
        int dot = params.indexOf(',');
        String type = params.substring(0, dot);
        String pinStr = params.substring(dot + 2);
        int pin = pinStr.toInt();

        if (type == "an") {
            int value = analogRead(pin);
            Serial.println(value);
        } else if (type == "dg") {
            int value = digitalRead(pin);
            Serial.println(value);
        }
    }

    static void write(const String &params) {
        int firstDot = params.indexOf(',');
        int secondDot = params.indexOf(',', firstDot + 1);

        String type = params.substring(0, firstDot);
        String pinStr = params.substring(firstDot + 2, secondDot);
        String valueStr = params.substring(secondDot + 2);

        int pin = pinStr.toInt();
        int value = valueStr.toInt();

        if (type == "an") {
            analogWrite(pin, value);
        } else if (type == "dg") {
            digitalWrite(pin, value == 1 ? HIGH : LOW);
        }
    }
};



// Вспомогательные функции
bool isNumber(const String &str) {
    return str.length() > 0 && (str.toInt() != 0 || str == "0");
}

float calculate(const String &params) {
    int firstSpace = params.indexOf(' ');
    int secondSpace = params.indexOf(' ', firstSpace + 1);

    String firstParamStr = params.substring(0, firstSpace);
    String operand = params.substring(firstSpace + 1, secondSpace);
    String secondParamStr = params.substring(secondSpace + 1);

    if (isNumber(firstParamStr) && isNumber(secondParamStr)) {
        float firstParam = firstParamStr.toFloat();
        float secondParam = secondParamStr.toFloat();

        if (operand == "+") return firstParam + secondParam;
        if (operand == "-") return firstParam - secondParam;
        if (operand == "*") return firstParam * secondParam;
        if (operand == "/") return secondParam != 0 ? firstParam / secondParam : 0;
    }
    return 0;
}

// Парсер
class CommandParser {
public:
    void parse(const String &args) {
        if (args.indexOf('.') != -1) {
            int dot = args.indexOf('.');
            int startParams = args.indexOf('(');
            int endParams = args.lastIndexOf(')');

            String command_1 = args.substring(0, dot);
            String command_2 = args.substring(dot + 1, startParams);
            String params = args.substring(startParams + 1, endParams);

            if (command_1 == "print") {
                if (command_2 == "Serial") {
                    MyPrint::printSerial(params);
                } else if (command_2 == "lnSerial") {
                    MyPrint::printlnSerial(params);
                }else{
                    Serial.println("Error: command not found");
                }
            } else if(command_1 == "display"){
                if (command_2 == "print") {
                    Display::displayText(params);
                } else if (command_2 == "rect") {
                    Display::displayRect(params);
                } else if (command_2 == "pixel") {
                    Display::displayPixel(params);
                } else if (command_2 == "clear") {
                    Display::displayClear();
                } else {
                    Serial.println("Error: command not found");
                }
            } else if (command_1 == "pin") {
                if (command_2 == "read") {
                    Pin::read(params);
                } else if (command_2 == "write") {
                    Pin::write(params);
                } else if (command_2 == "init") {
                    Pin::init(params);
                } else {
                    Serial.println("Error: command not found");
                }
            } else {
                Serial.println("Error: command not found");
            }
        } else {
            Serial.println("Error: command not found");
        }
    }
};

// Глобальные объекты
CommandParser commandParser;
