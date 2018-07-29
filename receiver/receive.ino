bool val = 0;  // variable to store the value read
const int frequenz = 100; //Hz
const int laengeNachricht = 800;
bool nachrichtArray[laengeNachricht];
int zaehlerNachricht = 0;
int inputPin = 0;// anderen angeben

unsigned long startTime;
unsigned long currentTime;

unsigned long referenceTime;

void setup()
{

 Serial.begin(9600);
 Serial.println("Start"); //  setup serial
 pinMode(inputPin, INPUT);
 val = digitalRead(inputPin);
 while (val == false){
   val = digitalRead(inputPin);
 }
 startTime = millis();
 startTime += 5000;
 while (val == true){
   val = digitalRead(inputPin);
 }
 currentTime = millis();

 if (currentTime < startTime){
   Serial.println("Mies! Fail!");
 }
 //startTime = millis();
 startTime += 500;
 while (val == false){
   val = digitalRead(inputPin);
 }
 currentTime = millis();
 if (currentTime < startTime) {
   Serial.println("Mies! Fail!");  
 }
 startTime += 100;
 startTime += (1 / frequenz) / 2; // damit in der Mitte gemessen wird
 //mit Zeit arbeitne statt zu messen
 while(currentTime < startTime){
   currentTime = millis();
 }

}

void loop()
{
 val = digitalRead(inputPin);
 nachrichtArray[zaehlerNachricht] = val;
 zaehlerNachricht += 1;
 while (zaehlerNachricht < (laengeNachricht - 1)){
   //startTime = millis();
   //val = digitalRead(inputPin);// read the input pin
   //nachrichtArray[i] = val;
   currentTime = millis();
   //nicht jeder messwert ist neue Nachricht?

   if (currentTime > referenceTime) {

     val = digitalRead(inputPin);
     //
     if (val == true){
       nachrichtArray[zaehlerNachricht] = true;
     } 
     else if (val == false){

       nachrichtArray[zaehlerNachricht] = false;
     }
     else {
       Serial.println("Fail");
     }
     zaehlerNachricht += 1;
     referenceTime = startTime + (zaehlerNachricht * (1000 / frequenz));

   }
 }


 //wenn das Programm fertig ist
 if (zaehlerNachricht >= laengeNachricht - 1){
   Serial.println("Fertig");
   int byteArrayLaenge = laengeNachricht / 8;
   byteArrayLaenge = (int) byteArrayLaenge;
   int byteZaehler = 0;
   bool byteArray[byteArrayLaenge];
   int ord = 0;
   String outputString = "";
   for(int i = 0; i < laengeNachricht; i++){
     Serial.println(nachrichtArray[i]); 
     ord += pow(2, (8 - byteZaehler));
     if (byteZaehler >= 7) {
       byteZaehler = 0;
       char meinchar = char(ord);
       outputString += meinchar;
       //Serial.write(ord);
       ord = 0;

     }else{
     byteZaehler += 1;
     }
   }


   //break;
   Serial.println(outputString);
 }

}
