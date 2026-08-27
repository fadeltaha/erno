const int ROWS = 2;
const int COLUMNS = 10;

String buffer_array[ROWS][COLUMNS];

void pattern_1() {
  for (int i = 2; i < 8; i++) {
    digitalWrite(i, HIGH);
    delay(100);
    digitalWrite(i, LOW);
  }
  for (int i = 7; i > 1; i--) {
    digitalWrite(i, HIGH);
    delay(100);
    digitalWrite(i, LOW);
  }
}

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  Serial.begin(9600);
  pattern_1();
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    int spaceIdx = data.indexOf(' ');
    if (spaceIdx <= 0) return;  // malformed line, no space found — bail out

    String move = data.substring(0, spaceIdx);
    long moveTime = data.substring(spaceIdx + 1).toInt();

    if (move == "R" || move == "R'") {
      digitalWrite(2, HIGH);
      delay(moveTime);
      digitalWrite(2, LOW);
      delay(moveTime);
      digitalWrite(2, HIGH);
      delay(moveTime);
      digitalWrite(2, LOW);
    }
    if (move == "L" || move == "L'") {
      digitalWrite(3, HIGH);
      delay(moveTime);
      digitalWrite(3, LOW); 
      delay(moveTime);
      digitalWrite(3, HIGH);
      delay(moveTime);
      digitalWrite(3, LOW);
    }
    if (move == "U" || move == "U'") {
      digitalWrite(4, HIGH);
      delay(moveTime);
      digitalWrite(4, LOW);
      delay(moveTime);
      digitalWrite(4, HIGH);
      delay(moveTime);
      digitalWrite(4, LOW);
    }
    if (move == "D" || move == "D'") {
      digitalWrite(5, HIGH);
      delay(moveTime);
      digitalWrite(5, LOW);
      delay(moveTime);
      digitalWrite(5, HIGH);
      delay(moveTime);
      digitalWrite(5, LOW);
    }
    if (move == "F" || move == "F'") {
      digitalWrite(6, HIGH);
      delay(moveTime);
      digitalWrite(6, LOW);
      delay(moveTime);
      digitalWrite(6, HIGH);
      delay(moveTime);
      digitalWrite(6, LOW);
    }
    if (move == "B" || move == "B'") {
      digitalWrite(7, HIGH);
      delay(moveTime);
      digitalWrite(7, LOW);
      delay(moveTime);
      digitalWrite(7, HIGH);
      delay(moveTime);
      digitalWrite(7, LOW);
    }
  }
}