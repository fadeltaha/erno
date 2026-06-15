const int ROWS = 2;
const int COLUMNS = 10;

String buffer_array[ROWS][COLUMNS];

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim()
    if (data == "R" || data == "R'") {
      digitalWrite(2, HIGH);
      delay(100);
      digitalWrite(2, LOW);
    }
    if (data == "L" || data == "L'") {
      digitalWrite(3, HIGH);
      delay(100);
      digitalWrite(3, LOW);
    }
    if (data == "U" || data == "U'") {
      digitalWrite(4, HIGH);
      delay(100);
      digitalWrite(4, LOW);
    }
    if (data == "D" || data == "D'") {
      digitalWrite(5, HIGH);
      delay(100);
      digitalWrite(5, LOW);
    }
    if (data == "F" || data == "F'") {
      digitalWrite(6, HIGH);
      delay(100);
      digitalWrite(6, LOW);
    }
    if (data == "B" || data == "B'") {
      digitalWrite(7, HIGH);
      delay(100);
      digitalWrite(7, LOW);
    }
  }
}

