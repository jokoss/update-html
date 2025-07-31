$(function(){
  // Function to determine the correct path depth
  function getPathDepth() {
    var path = window.location.pathname;
    var depth = (path.match(/\//g) || []).length - 1;
    
    // If we're in a subdirectory, we need to go up
    if (path.includes('/services/') || path.includes('/about-us/') || 
        path.includes('/contact-us/') || path.includes('/forms/') || 
        path.includes('/sampling/') || path.includes('/sampling-info/') ||
        path.includes('/laboratorytesting/')) {
      
      // Check if we're in a nested subdirectory (like /services/agriculture/)
      var pathParts = path.split('/').filter(part => part !== '');
      if (pathParts.length > 2) {
        return "../../";
      } else if (pathParts.length > 1) {
        return "../";
      }
    }
    
    // If we're at root level
    return "./";
  }
  
  var basePath = getPathDepth();
  
  $("#header").load(basePath + "header.html");
  $("#footer").load(basePath + "footer.html");
});
