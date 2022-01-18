var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("act");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}
var sel1 = document.querySelectorAll('[id$="_fillna"]');
console.log(sel1)
for (i = 0; i < sel1.length; i++) {
    sel1[i].addEventListener('click', function() {
        let con = this.nextElementSibling.nextElementSibling
        console.log(con)
        con.style.display = "block";

    });
}
var sel1 = document.querySelectorAll('[id$="_dropna"]');
for (i = 0; i < sel1.length; i++) {
    sel1[i].addEventListener('click', function() {
        let con = this.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling
        console.log(con)
        con.style.display = "none";

    });
}