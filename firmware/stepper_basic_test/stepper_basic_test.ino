// pins match grbl default x axis on the uno
const int stepPin = 2;
const int dirPin = 5;
const int enablePin = 8;

const int fullSteps = 200;     // 1.8 deg nema 17
int microsteps = 16;           // match the driver jumpers
long stepDelayUs = 800;        // lower = faster
bool enabled = true;

long stepsPerRev() {
  return (long)fullSteps * microsteps;
}

void setEnable(bool on) {
  enabled = on;
  digitalWrite(enablePin, on ? LOW : HIGH);   // active low
}

void moveSteps(long n) {
  digitalWrite(dirPin, n > 0 ? HIGH : LOW);
  delayMicroseconds(5);   // dir setup time

  for (long i = 0; i < labs(n); i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelayUs);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelayUs);
  }
}

void printSettings() {
  Serial.print("steps/rev: ");
  Serial.println(stepsPerRev());
  Serial.print("step delay us: ");
  Serial.println(stepDelayUs);
  Serial.print("enabled: ");
  Serial.println(enabled);
}

void runTest() {
  moveSteps(stepsPerRev());      // 1 rev forward
  delay(500);

  moveSteps(-stepsPerRev());     // 1 rev back
  delay(500);

  moveSteps(stepsPerRev() / 2);  // half rev out
  delay(250);

  moveSteps(-stepsPerRev() / 2); // half rev back, should end at start
  Serial.println("test done");
}

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  setEnable(true);

  Serial.begin(115200);
  Serial.println("f/r = 1 rev, s <n> = n steps, v <us> = speed, t = test, e = enable, ? = settings");
  printSettings();
}

void loop() {
  if (!Serial.available()) return;
  char c = Serial.read();

  if (c == 'f') moveSteps(stepsPerRev());        // forward
  else if (c == 'r') moveSteps(-stepsPerRev());  // reverse
  else if (c == 's') moveSteps(Serial.parseInt());
  else if (c == 'v') {
    long us = Serial.parseInt();
    if (us >= 50) stepDelayUs = us;              // below 50 us it skips
  }
  else if (c == 't') runTest();
  else if (c == 'e') setEnable(!enabled);
  else if (c == '?') printSettings();
}
