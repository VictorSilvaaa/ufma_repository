<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">

  <title>Logis Bootstrap Template - Index</title>
  <meta content="" name="description">
  <meta content="" name="keywords">

  <!-- Favicons -->
  <link href="resources/img/favicon.png" rel="icon">
  <link href="resources/img/apple-touch-icon.png" rel="apple-touch-icon">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,600;1,700&family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">

  <!-- Vendor CSS Files -->
  <link href="resources/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <link href="resources/vendor/bootstrap-icons/bootstrap-icons.css" rel="stylesheet">
  <link href="resources/vendor/fontawesome-free/css/all.min.css" rel="stylesheet">
  <link href="resources/vendor/glightbox/css/glightbox.min.css" rel="stylesheet">
  <link href="resources/vendor/swiper/swiper-bundle.min.css" rel="stylesheet">
  <link href="resources/vendor/aos/aos.css" rel="stylesheet">

  <!-- Template Main CSS File -->
  <link href="resources/css/main.css" rel="stylesheet">

  <!-- =======================================================
  * Template Name: Logis
  * Updated: Sep 18 2023 with Bootstrap v5.3.2
  * Template URL: https://bootstrapmade.com/logis-bootstrap-logistics-website-template/
  * Author: BootstrapMade.com
  * License: https://bootstrapmade.com/license/
  ======================================================== -->
</head>

  <body>
  <div class="container mb-60">
          
      <div class="panel panel-primary">
      
        <div class="panel-heading">
          <h2>Converter Word Dox File para PDF</h2>
        </div>
      
        <div class="panel-body">
            
          <form action="{{ route('converter') }}" method="POST" enctype="multipart/form-data">
              @csrf
      
              <div class="mb-3">
                  <strong class="form-label" for="inputFile">Upload arquivo Word:</strong>
                  <input 
                      type="file" 
                      name="file" 
                      id="inputFile">
              </div>
      
              <div class="mb-3">
                  <button type="submit" class="btn btn-success">Converter</button>
              </div>
          
          </form>
          
        </div>
      </div>
  </div>
  
  </body>
</html>


<!--  
<body>
<div class="container mb-60">
         
    <div class="panel panel-primary">
    
      <div class="panel-heading">
        <h2>Converter Word Dox File para PDF</h2>
      </div>
    
      <div class="panel-body">
          
        <form action="{{ route('converter') }}" method="POST" enctype="multipart/form-data">
            @csrf
    
            <div class="mb-3">
                <strong class="form-label" for="inputFile">Upload arquivo Word:</strong>
                <input 
                    type="file" 
                    name="file" 
                    id="inputFile">
            </div>
     
            <div class="mb-3">
                <button type="submit" class="btn btn-success">Converter</button>
            </div>
        
        </form>
        
      </div>
    </div>
</div>
 
</body>
 -->