function getPixel(img, x, y) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    context.drawImage(img, 0, 0);
    return context.getImageData(x, y, 1, 1).data;
}

async function fetchImage(){
    const response = await fetch('/get_tile');
    const json = await response.json();

    console.log(json);

    var image = document.getElementById("ch_img")
    image.src = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + json.year + "/MapServer/tile/11/" + json.y + "/" + json.x;
    image.crossOrigin = '';

    // If the image is empty (transparent), load a new one
    image.onload = function(){
        var pixelAlpha = getPixel(image, 1, 1)[3]
        if(pixelAlpha == 0) fetchImage();
    }

    // If the image fails to load, load a new one
    image.onerror = function(){
        fetchImage();
    }
}

async function check(){
    await fetchImage();

    var popup = document.getElementById("challenge1");
    popup.classList.toggle("show");
}