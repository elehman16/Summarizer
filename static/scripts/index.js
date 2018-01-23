/**
* Summarize the text.
*/
function summarize() {
  var text = document.getElementById("text-to-summarize").value;
  if (text === undefined || text === '') {
    return ;
  } else {
    post("/summarize/", {"text-to-summarize": text})
  }
}

function upload() {
  document.getElementById("fileInput").click();
}

function key_vocab() {
  var text = document.getElementById("text-to-summarize").value;
  if (text === undefined || text === '') {
    return ;
  } else {
    post("/key_vocab/", {"text-to-summarize": text})
  }
}

document.getElementById("fileInput").onchange = function() {
    document.getElementById("form").submit();
}

$("#upload-but").click(upload);
$("#summary-but").click(summarize);
$("#key-vocab-but").click(key_vocab);
