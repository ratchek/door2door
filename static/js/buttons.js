function hi() {
  alert("hi-hi");
}

function changeForm() {
  document.getElementById("id_address-house_number").value = "My value";
}

function up() {
  updtateHouseNumber(2);
}

function down() {
  updtateHouseNumber(-2);
}

function updtateHouseNumber(val) {
  // Change so that stuff like 36-63 works as expected (you'll need to extract the number, increment it, then put it back in.)
  // Right now the if statement is creating an endless 0 when 0 happens to be the number. Fix that
  var new_value;
  var numbers = document.getElementById("id_address-house_number").value;
  var initial_value = parseInt(numbers);
  if (initial_value) {
    new_value = initial_value + val;
  } else {
    new_value = initial_value;
  }
  document.getElementById("id_address-house_number").value = new_value;
  console.log("initial value = ", initial_value);
  console.log("new value = ", new_value);
}
