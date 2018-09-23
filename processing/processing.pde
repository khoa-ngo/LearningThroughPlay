import processing.serial.*;
import grafica.*;

boolean PLOT = true;
boolean LOG = true;
boolean DEBUG = false;

// Plotting
GPlot plot;
int npoints = 200;  // number of points to be plotted
float scale_y = 20;  // plot scaling for y values
boolean updated = false;  // check for update before plotting
int step = 0;
float last_time;
float current_time;
int laststep=0;
float lasty=0;

// Serial Comm
Serial myPort;
int baudrate = 115200; // serial comm between Arduino and PC
float angle;
float rate;
float action;
float Data[];
String[] inData;

// Logging
String filename = "log1.txt";
PrintWriter output;

void setup () {
  // Plotting
  size(700, 700);
  if (PLOT) {
    GPointsArray points1 = new GPointsArray(npoints);
    for (int i = 0; i < npoints; i++) {
      points1.add(calculatePoint(angle));
      step++;
    }
    plot = new GPlot(this);
    plot.setPos(0, 0);
    plot.setDim(600, 600);
    plot.setYLim(-1.1*scale_y, 1.1*scale_y);
    plot.setXLim(0, npoints);
    plot.setTitleText("Title");
    plot.getXAxis().setAxisLabelText("x axis");
    plot.getYAxis().setAxisLabelText("y axis");
    plot.activatePanning();
    plot.setPoints(points1);
  }
  
  // Serial Comm
  print(Serial.list());
  myPort = new Serial(this, Serial.list()[1], 115200);
  //myPort.bufferUntil('\n');
  
  // Logging
  if (LOG) {
    output = createWriter(filename);
  }
  
  // Debug
  if (DEBUG) {updateTimer();}
}

void draw () {
  // Debug
  if (DEBUG) {println(updateTimer());}
  
  // Plotting
  if (PLOT && updated) {
    scatter_plot(plot);
  }
  
  //Logging
  if (LOG) {
    
  }
}

void exit() {
  output.close();
  super.exit();
}

void serialEvent (Serial myPort) {
  String inString = myPort.readStringUntil('\n');
  if (inString != null) {
    inString = trim(inString);
    inData = splitTokens(inString, "\t");
    angle = float(inData[0]);  // Angle
    rate = float(inData[1]);  // Rate
    action = float(inData[2]);  // Action
    output.println(angle + " " + rate + " " + action);
    output.flush();
    //angle = map(angle, 0, 90000, 0, 90);
    //rate = map(rate, 0, 50, 0, 100);
    updated = true;
  }
}

GPoint calculatePoint(float a) {
  return new GPoint(step, a);
}

void scatter_plot(GPlot plot) {
  background(150);
  plot.beginDraw();
  plot.drawBackground();
  plot.drawBox();
  plot.drawXAxis();
  plot.drawYAxis();
  plot.drawTopAxis();
  plot.drawRightAxis();
  plot.drawTitle();
  plot.getMainLayer().drawPoints();
  plot.endDraw();
  plot.setXLim(step - npoints, step);
  plot.addPoint(calculatePoint(angle));
  step++;
  plot.removePoint(0);
  updated = false;
}

float updateTimer() {
  float current_time = millis();
  float delta_time = current_time - last_time;
  last_time = current_time;
  return delta_time;
}
