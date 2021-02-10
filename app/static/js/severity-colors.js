// Run function on load
window.onload = function(){

  // Info
  var info = document.getElementsByName("Info");
  // Low
  var low = document.getElementsByName("Low");
  // Medium
  var medium = document.getElementsByName("Medium");
  // High
  var high = document.getElementsByName("High");
  // Critical
  var crit = document.getElementsByName("Critical");

  info.style.backgroundColor = 'rgb(0, 113, 185)'
  low.style.backgroundColor = 'rgb(63, 174, 73)'
  medium.style.backgroundColor = 'rgb(253, 196, 49)'
  high.style.backgroundColor = 'rgb(238, 147, 54)'
  crit.style.backgroundColor = 'rgb(212, 63, 58)'
}();