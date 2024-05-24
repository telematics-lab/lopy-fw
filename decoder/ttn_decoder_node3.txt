function Decoder(bytes, port) {
  
  var latitude = {}
  var longitude = {}
  
  latitude.lat1 = ((bytes[1] << 8) + bytes[0]);
  latitude.lat2 = ((bytes[2] << 8) + bytes[3]);
  latitude.lat3 = ((latitude.lat2 << 8) + (latitude.lat1))/100000;
  
  longitude.long1 = ((bytes[5] << 8) + bytes[4]);
  longitude.long2 = ((bytes[6] << 8) + bytes[7]);
  longitude.long3 = ((longitude.long2 << 8) + (longitude.long1))/100000;
  
  const float32 = new Float32Array(4);
  const float32long = new Float32Array(4);
  float32[0] = latitude.lat3;
  float32long[0] = longitude.long3;
  
  return {
    latitude: float32[0],
    longitude: float32long[0]
  };
}