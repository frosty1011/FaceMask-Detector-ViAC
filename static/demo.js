var child1 = document.getElementById("top-container");
var parent = document.getElementById("particles-js");

console.log("CHILD 1",child1);

var childHeight = parseInt(window.getComputedStyle(child1).height) + "px";

console.log("CHILD HEIGHT",childHeight);

parent.style.height = childHeight;