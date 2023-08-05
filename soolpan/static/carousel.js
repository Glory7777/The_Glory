(() => {
    const carouselImages = document.querySelectorAll('.carousel-image');
    let currentImageIndex = 0;

    function showNextImage() {
        carouselImages[currentImageIndex].classList.remove('active');
        currentImageIndex = (currentImageIndex + 1) % carouselImages.length;
        carouselImages[currentImageIndex].classList.add('active');
    }
    setInterval(showNextImage, 5000);
})();    