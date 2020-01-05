function addImage(appendId, path, desc, width, height) {
    var newDiv = document.createElement("div");
    newDiv.className = "img-div";
    newDiv.style.width = width;
    newDiv.style.height = height;

    var img = new Image();
    img.style.width = width;
    img.style.height = height;
    img.src = path;
    img.className = "img-loaded";
    newDiv.appendChild(img);

    var textDiv = document.createElement("div");
    textDiv.className = "text-div";
    textDiv.innerHTML = desc;
    newDiv.appendChild(textDiv);

    document.getElementById(appendId).appendChild(newDiv);
}

function getSmallestColumn(colHeights) {
    var smallestIndex = 0;
    var minHeight = Number.MAX_VALUE;
    for (var i = 0; i < colHeights.length; i++) {
        if (colHeights[i] === 0) {
            return i;
        }
        if (colHeights[i] < minHeight) {
            smallestIndex = i;
            minHeight = colHeights[i];
        }
    }
    return smallestIndex;
}

function addAlbum(name, data) {
    var albumDiv = document.createElement("div");
    albumDiv.id = name;

    var header = document.createElement("h3");
    header.innerHTML = name;
    albumDiv.appendChild(header);

    var imgDiv = document.createElement("div");
    imgDiv.className = "img-columns";
    albumDiv.appendChild(imgDiv);

    var col0 = document.createElement("div");
    col0.id = name + " col0";
    col0.style.width = "500px";
    imgDiv.appendChild(col0);

    var col1 = document.createElement("div");
    col1.id = name + " col1";
    col1.style.width = "500px";
    imgDiv.appendChild(col1);

    var col2 = document.createElement("div");
    col2.id = name + " col2";
    col2.style.width = "500px";
    imgDiv.appendChild(col2);

    document.getElementById("gallery").appendChild(albumDiv);

    var colHeights = new Array(3).fill(0);

    for (var i = 0; i < data.length; i++) {
        var column = getSmallestColumn(colHeights);
        var appendId = name + " col" + column;
        var width = 500;
        var height = 500 * data[i]["height"] / data[i]["width"];
        colHeights[column] += height;
        addImage(appendId, data[i]["path"], data[i]["desc"], width + "px", height + "px");
    }
}

function reqListener() {
  var config = JSON.parse(this.responseText);
  for (key in config) {
      addAlbum(key, config[key]);
  }
  lazyload();
}

window.onload = function() {
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("GET", "config.json");
    oReq.send();
};
