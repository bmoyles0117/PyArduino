int serial_int = 0;
String serial_msg = "";
char serial_chars[100];
char serial_char = ' ';


const int DIGITAL_READ = 1;
const int DIGITAL_WRITE = 2;
const int PIN_MODE = 3;
const int ANALOG_READ = 4;
const int ANALOG_WRITE = 5;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(5);
  
  serial_msg = "";
}

void loop() {
  if(Serial.available() <= 0)
    return;

  serial_int = Serial.read();
  serial_char = serial_int;
  serial_msg = "";
  
  while(true) {
    while(serial_int == -1) {
      serial_char = Serial.read();
      serial_int = serial_char;
    }

    if(serial_char == ':')
      break;
     
    serial_msg += serial_char;
      
    serial_char = Serial.read(); 
    serial_int = serial_char;
  }
  
  int message_size = serial_msg.toInt();
  
  Serial.readBytes(serial_chars, message_size);

  int instruction_index = 0, last_index = 0;
  
  String instructions[3] = {"", "", ""};

  for(int i = 0; i < message_size; i++) {
    serial_char = serial_chars[i];

    if(serial_char == ',') {
      instruction_index += 1;
    } else {
      instructions[instruction_index] += serial_char;
    }
  }

  handle_instructions(instructions, instruction_index + 1);
}

void handle_instructions(String instructions[], int total_instructions) {
  int command = instructions[0].toInt();
  
  switch(command) {
    case ANALOG_WRITE:
      analogWrite(instructions[1].toInt(), instructions[2].toInt());
    break;
    case DIGITAL_READ:
      Serial.println(digitalRead(instructions[1].toInt()));
    break;
    case DIGITAL_WRITE:
      // Serial.println("digitalWrite(" + instructions[1] + ", " + instructions[2] + ")");
      digitalWrite(instructions[1].toInt(), instructions[2].toInt() == 1 ? HIGH : LOW);
    break;
    case PIN_MODE:
      // Serial.println("pinMode(" + instructions[1] + ", " + instructions[2] + ")");
      pinMode(instructions[1].toInt(), instructions[2].toInt() == 1 ? OUTPUT : INPUT);
    break;
  }
}
