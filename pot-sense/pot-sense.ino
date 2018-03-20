int potPin = 3;
int val;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = analogRead(potPin);
  Serial.print("\nvalue: ");
  Serial.print(val);

}
