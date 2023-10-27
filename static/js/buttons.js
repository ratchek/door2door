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
  // Get the value entered into the house_number field
  var house_number = document.getElementById("id_address-house_number").value;
  // Get the last number that occurs (for example for 23-15N, this will return 15)
  var just_numbers = house_number.match(/\d+/g);
  // Make sure there's some numbers in the string!
  if (just_numbers == null) {
    alert(
      "I don't know how to change that house number!\nPlease input it by hand."
    );
  } else {
    var old_number = just_numbers.pop();
    var new_number = parseInt(old_number) + val;
    if (new_number < 0) {
      alert(
        "I don't know how to change that house number!\nPlease input it by hand."
      );
    } else {
      // Insert the new (increased or decreased) number into the full house number.
      // So if I'm increasing 23-18N, I should get 23-20N
      var new_house_number = house_number.replace(
        /\d+(\D*)$/,
        new_number + "$1"
      );
      document.getElementById("id_address-house_number").value =
        new_house_number;
    }
  }
}
