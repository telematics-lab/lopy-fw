function Decoder(bytes, port) {

  var temp_1 = bytes[0];
  var temp_2 = bytes[1];
  
  var hum_1 = bytes[2];
  var hum_2 = bytes[3];
  
  var temp = (temp_2 << 8) | temp_1;
  var hum = (hum_2 << 8) | hum_1;
  
  const int16 = new Int16Array(2);
  int16[0] = temp;
  int16[1] = hum;

  return {
    temperature: int16[0] /10,
    humidity: int16[1]/10
  };
}