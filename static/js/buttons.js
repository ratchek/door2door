function hi() {
  alert("hi-hi");
}

function changeForm() {
  document.getElementById("id_address-house_number").value = "My value";
}

function up() {
  initial_value = parseInt(
    document.getElementById("id_address-house_number").value
  );
  document.getElementById("id_address-house_number").value = initial_value + 2;
}

function down() {
  initial_value = parseInt(
    document.getElementById("id_address-house_number").value
  );
  document.getElementById("id_address-house_number").value = initial_value - 2;
}
