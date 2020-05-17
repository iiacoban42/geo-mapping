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

    var image1 = document.getElementById("ch_img1")
    image1.src = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + json[0].year + "/MapServer/tile/11/" + json[0].y + "/" + json[0].x;
    image1.crossOrigin = '';

    // If the image is empty (transparent), load a new one
    image1.onload = function(){
        var pixelAlpha = getPixel(image1, 1, 1)[3]
        if(pixelAlpha == 0) fetchImage();
    }

    // If the image fails to load, load a new one
    image1.onerror = function(){
        fetchImage();
    }

    var image2 = document.getElementById("ch_img2")
    image2.src = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + json[1].year + "/MapServer/tile/11/" + json[1].y + "/" + json[1].x;
    image2.crossOrigin = '';

     // If the image is empty (transparent), load a new one
    image2.onload = function(){
        var pixelAlpha = getPixel(image2, 1, 1)[3]
        if(pixelAlpha == 0) fetchImage();
    }

    // If the image fails to load, load a new one
    image2.onerror = function(){
        fetchImage();
    }
}

async function check(){
    await fetchImage();

    var popup = document.getElementById("challenge1");
    popup.classList.toggle("show"); 
}

async function next(){
    var popup1 = document.getElementById("challenge1");
    popup1.classList.toggle("show");

    var popup2 = document.getElementById("challenge2");
    popup2.classList.toggle("show");
}