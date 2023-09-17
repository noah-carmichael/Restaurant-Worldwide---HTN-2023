// Arduino pin numbers
const int SW_pin = 8; // digital pin connected to switch output
const int X_pin = 0; // analog pin connected to X output
const int Y_pin = 1; // analog pin connected to Y output
// String x;
// #include <LiquidCrystal.h>
// LiquidCrystal lcd(6, 7, 8, 9, 10, 11);

void setup() {
  pinMode(SW_pin, INPUT);
  digitalWrite(SW_pin, HIGH);

  // lcd.begin(16, 2);
  // lcd.clear();
  // lcd.setCursor(0, 0);
  // lcd.print("Starting Hotlap ");
  // lcd.setCursor(0, 1);
  // lcd.print("    Timer...  ");
  // delay(1000);
  // lcd.clear();

  Serial.begin(9600);

}

void loop() {
  // Serial.print("Switch:  ");
  // Serial.print(digitalRead(SW_pin));
  // Serial.print(" | ");
  // Serial.print("X-axis: ");
  Serial.println(analogRead(X_pin));
  
  // Serial.print(" | ");
  // Serial.print("Y-axis: ");
  // Serial.println(analogRead(Y_pin));
  // Serial.println(" | ");

  //   while (!Serial.available());
  // x = Serial.readString();
  // lcd.print(x);
  delay(200);
}
