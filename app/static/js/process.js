document.addEventListener('DOMContentLoaded', () => {
  const imageUpload = document.getElementById('imageUpload');
  const fileName = document.getElementById('fileName');
  const processButton = document.getElementById('processButton');
  const downloadSection = document.getElementById('downloadSection');
  const processedImage = document.getElementById('processedImage');
  const downloadButton = document.getElementById('downloadButton');
  const downloadCSVButton = document.getElementById('downloadCsvButton'); // CSV download button

  let uploadedImagePath = '';

  // Event listener for file selection
  imageUpload.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
      fileName.textContent =
        file.name.length > 30 ? file.name.substring(0, 27) + '...' : file.name;
      processButton.classList.remove('disabled');
      processButton.removeAttribute('disabled');
      uploadedImagePath = URL.createObjectURL(file); // Create object URL for the image
    } else {
      fileName.textContent = 'No file chosen';
      processButton.classList.add('disabled');
      processButton.setAttribute('disabled', 'true');
    }
  });

  // Event listener for clicking the process button
  processButton.addEventListener('click', async () => {
    const formData = new FormData();
    formData.append('image', imageUpload.files[0]);

    try {
      const response = await fetch('/process', {
        method: 'POST', // Ensure a POST request is sent
        body: formData,
      });

      const result = await response.json();

      if (result.processed_image) {
        // Display processed image and download button
        processedImage.src = result.processed_image;
        downloadSection.style.display = 'block';
        downloadButton.href = result.processed_image;

        // Add handling for CSV file download
        const filename = result.processed_image.split('/').pop(); // Get the processed file name
        downloadCSVButton.href = `/download_detected_info?filename=${filename}`;
        downloadCSVButton.style.display = 'inline-block'; // Show CSV button
      } else {
        alert('Error processing the image.');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });
});
