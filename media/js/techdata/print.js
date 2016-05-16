function pagePrint(data) {
    var bodyHTML = window.document.body.innerHTML;
    window.document.body.innerHTML = data;
    window.print();
    window.document.body.innerHTML = bodyHTML;
}
