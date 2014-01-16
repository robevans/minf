import processing.opengl.*;

int dataNum = 0;
int drawRate = 81;

JSONArray L_pitches;
JSONArray L_rolls;
JSONArray R_pitches;
JSONArray R_rolls;

float L_pitch =0;
float L_roll =0;
float R_pitch =0;
float R_roll =0;

float[][] L_trail;
float[][] R_trail;

int L_index = 0;
int R_index = 0;

int startTimer;
 
void setup(){
size(1500, 800, OPENGL);
smooth();
L_pitches = loadJSONArray("L/"+dataNum+"_pitch.json");
L_rolls = loadJSONArray("L/"+dataNum+"_roll.json");
R_pitches = loadJSONArray("R/"+dataNum+"_pitch.json");
R_rolls = loadJSONArray("R/"+dataNum+"_roll.json");
L_trail = new float[L_rolls.size()][3];
R_trail = new float[R_rolls.size()][3];
startTimer = millis();
}
 
void draw(){
  if ((millis() - startTimer) > drawRate) {
    background(0);
    lights();
    noStroke();
    
    pushMatrix();
    translate(width/2, height/2, 0);
    rotateY(L_roll);
    rotateX(L_pitch); 
    L_pitch = radians(L_pitches.getFloat(L_index));
    L_roll = radians(L_rolls.getFloat(L_index));
    translate(0, 60, 0);
    stroke(0,255,0);
    box(10,600,10);
    popMatrix();
    
    pushMatrix();
    translate(width/2, height/2, 0);
    rotateY(R_roll);
    rotateX(R_pitch); 
    R_pitch = radians(R_pitches.getFloat(R_index));
    R_roll = radians(R_rolls.getFloat(R_index));
    translate(0, 60, 0);
    stroke(255,0,0);
    box(10,600,10);
    popMatrix();
    
    float[] L_endOfNeedle = {0.0, 360.0, 0.0};
    L_endOfNeedle = rotatePointAboutXAxis(L_endOfNeedle, L_pitch);
    L_endOfNeedle = rotatePointAboutYAxis(L_endOfNeedle, L_roll);
    L_endOfNeedle[0] += width/2;
    L_endOfNeedle[1] += height/2;
    L_trail[L_index] = L_endOfNeedle;
    
    float[] R_endOfNeedle = {0.0, 360.0, 0.0};
    R_endOfNeedle = rotatePointAboutXAxis(R_endOfNeedle, R_pitch);
    R_endOfNeedle = rotatePointAboutYAxis(R_endOfNeedle, R_roll);
    R_endOfNeedle[0] += width/2;
    R_endOfNeedle[1] += height/2;
    R_trail[R_index] = R_endOfNeedle;
    
    for (int i=0; i<=L_index; i++) {
      stroke(0,255,0);
      point(L_trail[i][0], L_trail[i][1], L_trail[i][2]);
    }
    
    for (int i=0; i<=R_index; i++) {
      stroke(255,0,0);
      point(R_trail[i][0], R_trail[i][1], R_trail[i][2]);
    }
    
    if (L_index < L_pitches.size()-1) {
      L_index = (L_index + 1);
    }
    if (R_index < R_pitches.size()-1) {
      R_index = (R_index + 1);
    }
    startTimer = millis();
  }
}

float cameraYrotation = 0;
void keyPressed() {
  if (key == 'a') {
    cameraYrotation += 0.1;
  } else if (key =='d') {
    cameraYrotation -= 0.1;
  }
  float[] cameraCenter = {width/2.0, height/2.0, (height/2.0) / tan(PI*30.0 / 180.0)};
  cameraCenter[0] -= width/2;
  cameraCenter[1] -= height/2;
  cameraCenter = rotatePointAboutYAxis(cameraCenter, cameraYrotation);
  cameraCenter[0] += width/2;
  cameraCenter[1] += height/2;
  camera(cameraCenter[0], cameraCenter[1], cameraCenter[2], width/2.0, height/2.0, 0, 0, 1, 0);
}

float[] rotatePointAboutXAxis(float[] P, float radians) {
  float[][] Xrotate = {
  {1.0, 0.0, 0.0},
  {0.0, cos(radians), -sin(radians)},
  {0.0, sin(radians), cos(radians)}
  };
  return rotateAboutAxis(Xrotate, P);
}

float[] rotatePointAboutYAxis(float[] P, float radians) {
  float[][] Yrotate = {
  {cos(radians), 0.0, sin(radians)},
  {0.0, 1.0, 0.0},
  {-sin(radians), 0, cos(radians)}
  };
  return rotateAboutAxis(Yrotate, P);
}

float[] rotatePointAboutZAxis(float[] P, float radians) {
  float[][] Zrotate = {
  {cos(radians), -sin(radians), 0.0},
  {sin(radians), cos(radians), 0.0},
  {0.0, 0, 1.0}
  };
  return rotateAboutAxis(Zrotate, P);
}

float[] rotateAboutAxis(float[][] rotationMatrix, float[] P) {
  float[] R = new float[3];
  for (int r=0; r < R.length; r++) {
     for (int i=0; i < P.length; i++) {
       R[r] += rotationMatrix[r][i] * P[i];
     }
  }
  return R;
}

