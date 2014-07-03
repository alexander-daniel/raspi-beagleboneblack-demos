var plotly = require('plotly')('workshop','v6w5xlbx9j');
var five = require("johnny-five");
var board = new five.Board();

// plotly init data
var data = [
  {x:[], y:[], stream:{token:'25tm9197rz', maxpoints:500}},
  {x:[], y:[], stream:{token:'unbi52ww8a', maxpoints:500}}];
var layout = {fileopt : "overwrite", filename : "airquality nodey arduino!"};

// lets do this
board.on("ready", function() {
  // create a new `photoresistor` sensor object
  var airquality_sensor = new five.Sensor({
    pin: "A1",
    freq: 100 // send reading every 50ms
  });
  var gas_sensor = new five.Sensor({
    pin: "A0",
    freq: 100 // send reading every 50ms
  });
  // initialize that plotly graph
  plotly.plot(data,layout,function (err, res) {
    if (err) console.log(err);
    console.log(res);
    //once it's initialized, create a plotly stream
    //to pipe your data!
    var airquality_stream = plotly.stream('25tm9197rz', function (err, res) {
      if (err) console.log(err);
      console.log(res);
    });
    var gassensor_stream = plotly.stream('unbi52ww8a', function (err, res) {
      if (err) console.log(err);
      console.log(res);
    });
    // this gets called every time photoresistor returns its value
    airquality_sensor.on("data", function() {
      data = {
        x : getDateString(),
        y : this.value
      };
      // write the data to the plotly stream
      airquality_stream.write(JSON.stringify(data)+'\n');
    });
    gas_sensor.on("data", function() {
      data = {
        x : getDateString(),
        y : this.value
      };
      //console.log(this.value);
      // write the data to the plotly stream
      gassensor_stream.write(JSON.stringify(data)+'\n');
    });
  });
});

// little helper function to get a nicely formatted date string
function getDateString () {
  var time = new Date();
  // 14400000 is (GMT-4 Montreal)
  // for your timezone just multiply +/-GMT by 3600000
  var datestr = new Date(time - 14400000).toISOString().replace(/T/, ' ').replace(/Z/, '');
  return datestr;
}
