const images = [
    "https://source.unsplash.com/800x400/?farm",
    "https://source.unsplash.com/800x400/?crops",
    "https://source.unsplash.com/800x400/?agriculture"
];

let index = 0;
setInterval(() => {
    index = (index + 1) % images.length;
    document.getElementById("slide-img").src = images[index];
}, 3000);
