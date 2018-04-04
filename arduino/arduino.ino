float ob[4];

void setup() {
Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0) {
    String act = Serial.readStringUntil('\n');
//    float output = act.toFloat() * 2;
//    Serial.println(output);
    update(ob, act.toFloat());
    send(ob);
  }
}

void update(float (& ob)[4], float act) {
  // Function takes in action and update observation
  ob[0] = act * 1.0;
  ob[1] = act * 2.0;
  ob[2] = act * 3.0;
  ob[3] = act * 4.0;
}

void send(float (& ob)[4]) {
  for (int i=0; i<=3; i++){
    Serial.print(ob[i]);
    Serial.print(',');
    if (i==3) {
      Serial.println();
    }
  }
}

