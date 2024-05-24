function Decoder(bytes, port) {
  
  var light_1 = bytes[0];
  var light_2 = bytes[1];
  var decoded = {};
  
  var light1 = (light_2 << 8)|light_1;
  decoded.pressure  = ((bytes[3] << 8) + bytes[2]);
  decoded.pressure2 = ((bytes[4] << 8) + bytes[5]);
  decoded.pressure3 = ((decoded.pressure2<<8) + (decoded.pressure))/10;
  
  const int16 = new Int16Array(4);
  int16[0] = light1;
  
  const int32 = new Int32Array(4);
  int32[0] = decoded.pressure3;
      
  return {
	light: int16[0]*10,
	pressure: int32[0]    
  };
}