const int ROWS = 2;
const int COLUMNS = 10;

String buffer_array[ROWS][COLUMNS]

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.println(data)
  }
}
