// Run function on load
window.addEventListener("load", function(){
  // Info
  var info = document.getElementsByName("Info")
  var i;
  for (i = 0; i < info.length; i++) {
    info[i].classList.add('info');
  }
  
  // Low
  var low = document.getElementsByName("Low")
  var l;
  for (l = 0; l < low.length; l++) {
    low[l].classList.add('low');
  }

  // Medium
  var medium = document.getElementsByName("Medium")
  var m;
  for (m = 0; m < medium.length; m++) {
    medium[m].classList.add('medium');
  }

  // High
  var high = document.getElementsByName("High")
  var h;
  for (h = 0; h < high.length; h++) {
    high[h].classList.add('high');
  }

  // Critical
  var critical = document.getElementsByName("Critical")
  var c;
  for (c = 0; c < critical.length; c++) {
    critical[c].classList.add('critical');
  }
});