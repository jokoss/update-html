document.addEventListener('DOMContentLoaded', function() {
  // Function to determine the correct path depth
  function getPathDepth() {
    var path = window.location.pathname;
    
    // Count the number of directory levels from root
    var pathParts = path.split('/').filter(part => part !== '' && part !== 'index.html');
    
    // Remove the filename if present
    if (pathParts.length > 0 && pathParts[pathParts.length - 1].includes('.html')) {
      pathParts.pop();
    }
    
    // Generate the correct number of "../" based on depth
    var depth = pathParts.length;
    var basePath = '';
    for (var i = 0; i < depth; i++) {
      basePath += '../';
    }
    
    // If we're at root level, use current directory
    return basePath || './';
  }
  
  var basePath = getPathDepth();
  console.log('Navigation: Detected path depth, using basePath:', basePath);
  
  // Load header
  var headerElement = document.getElementById('header');
  if (headerElement) {
    fetch(basePath + 'header.html')
      .then(response => {
        if (!response.ok) {
          throw new Error('Header not found at: ' + basePath + 'header.html');
        }
        return response.text();
      })
      .then(data => {
        // Replace relative paths in header content based on current directory depth
        var updatedData = data.replace(/href="\.\/([^"]*)/g, 'href="' + basePath + '$1');
        updatedData = updatedData.replace(/src="\.\/([^"]*)/g, 'src="' + basePath + '$1');
        headerElement.innerHTML = updatedData;
        console.log('Navigation: Header loaded successfully');
        
        // Initialize Bootstrap components after header is loaded
        if (typeof bootstrap !== 'undefined') {
          var dropdowns = headerElement.querySelectorAll('[data-bs-toggle="dropdown"]');
          dropdowns.forEach(function(dropdown) {
            new bootstrap.Dropdown(dropdown);
          });
        }
      })
      .catch(error => {
        console.error('Error loading header:', error);
        // Fallback: try with different path
        fetch('../header.html')
          .then(response => response.text())
          .then(data => {
            var updatedData = data.replace(/href="\.\/([^"]*)/g, 'href="../$1');
            updatedData = updatedData.replace(/src="\.\/([^"]*)/g, 'src="../$1');
            headerElement.innerHTML = updatedData;
            console.log('Navigation: Header loaded with fallback path');
          })
          .catch(fallbackError => console.error('Fallback header load failed:', fallbackError));
      });
  }
  
  // Load footer
  var footerElement = document.getElementById('footer');
  if (footerElement) {
    fetch(basePath + 'footer.html')
      .then(response => {
        if (!response.ok) {
          throw new Error('Footer not found at: ' + basePath + 'footer.html');
        }
        return response.text();
      })
      .then(data => {
        // Replace relative paths in footer content based on current directory depth
        var updatedData = data.replace(/href="\.\/([^"]*)/g, 'href="' + basePath + '$1');
        updatedData = updatedData.replace(/src="\.\/([^"]*)/g, 'src="' + basePath + '$1');
        footerElement.innerHTML = updatedData;
        console.log('Navigation: Footer loaded successfully');
      })
      .catch(error => {
        console.error('Error loading footer:', error);
        // Fallback: try with different path
        fetch('../footer.html')
          .then(response => response.text())
          .then(data => {
            var updatedData = data.replace(/href="\.\/([^"]*)/g, 'href="../$1');
            updatedData = updatedData.replace(/src="\.\/([^"]*)/g, 'src="../$1');
            footerElement.innerHTML = updatedData;
            console.log('Navigation: Footer loaded with fallback path');
          })
          .catch(fallbackError => console.error('Fallback footer load failed:', fallbackError));
      });
  }
});