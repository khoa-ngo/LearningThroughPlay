import processing.serial.*;
import grafica.*;

GPlot plot;
int step = 0;
int npoints = 200;  // number of points to be plotted
float scale_y = 100;
boolean updated = false;
float last_time;
float current_time;

Serial myPort;
float inByte = 0.0;

int xPos = 1;
int lastxPos=0;
float lastheight=0;

void setup () {
  size(700, 700);

  myPort = new Serial(this, Serial.list()[1], 115200);
  myPort.bufferUntil('\n');
  
  GPointsArray points1 = new GPointsArray(npoints);
  
  for (int i = 0; i < npoints; i++) {
    points1.add(calculatePoint());
    step++;
  }
  
  plot = new GPlot(this);
  plot.setPos(0, 0);
  plot.setDim(600, 600);
  
  plot.setYLim(-1.2*scale_y, 1.2*scale_y);
  plot.setXLim(0, 40);
  
  plot.setTitleText("Title");
  plot.getXAxis().setAxisLabelText("x axis");
  plot.getYAxis().setAxisLabelText("y axis");
  
  plot.activatePanning();
  
  plot.setPoints(points1);
}

void draw () {
  if (updated) {
    current_time = millis();
    println(current_time - last_time);
    last_time = current_time;
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
    
    plot.addPoint(calculatePoint());
    step++;
  
    plot.removePoint(0);
    updated = false;
  }
}

void serialEvent (Serial myPort) {
  String inString = myPort.readStringUntil('\n');
  if (inString != null) {
    inString = trim(inString);
    inByte = float(inString);
    inByte = map(inByte, 0, 90000, 0, 90);
    //print(inByte);
    //print(' ');
    //println(inByte);
    updated = true;
  }
}

GPoint calculatePoint() {
  return new GPoint(step, inByte);
}
