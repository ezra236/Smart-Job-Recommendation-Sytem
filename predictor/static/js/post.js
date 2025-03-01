document.getElementById("company-logo").addEventListener("change", function () {
    let fileName = this.files.length > 0 ? this.files[0].name : "No file chosen";
    document.getElementById("file-name").textContent = fileName;
  });

 