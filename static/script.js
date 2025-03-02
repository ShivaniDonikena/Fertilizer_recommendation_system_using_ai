function predictDisease() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = new Image();
            img.src = e.target.result;
            img.onload = function() {
                // Here you would call your machine learning model to predict the disease
                // For now, let's just display a placeholder result
                document.getElementById('diseaseName').innerText = 'Placeholder: Detected Disease';
            };
        };
        reader.readAsDataURL(file);
    } else {
        alert('Please upload an image.');
    }
}
