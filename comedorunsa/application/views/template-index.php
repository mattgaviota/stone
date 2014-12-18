<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Sistema de tickets</title>
    <link href="<?= base_url('css/bootstrap.min.css'); ?>" rel="stylesheet" />
    <link href="<?= base_url('css/estilos.css'); ?>" rel="stylesheet" />
    
    <!--<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>-->
    <script src="<?= base_url('js/jquery.js'); ?>"></script>
    <script src="<?= base_url('js/bootstrap.min.js'); ?>"></script>
   
</head>
<body>

	<div class="navbar navbar-default navbar-fixed-top">
	    <div class="container">
	        <div class="navbar-header">
	          	<a class="navbar-brand glyphicon glyphicon-home" href="#"> UNSa</a>
	          	<button class="navbar-toggle" type="button" data-toggle="collapse" data-target="#navbar-main">
	            	<span class="icon-bar"></span>
	            	<span class="icon-bar"></span>
	            	<span class="icon-bar"></span>
	          	</button>
	          	
	        </div>

	        <div class="navbar-collapse collapse" id="navbar-main">
	          	<ul class="nav navbar-nav">
	          		<?= my_menu_principal(); ?>
	          	</ul>
	          	<ul class="nav navbar-nav navbar-right">
	          		<?= my_menu_principal_derecha(); ?>
	          	</ul>
	        </div>
	    </div>
	</div>

	<div class="container">
		<div class="page-header">
			<div class="row">
		        <!-- Menú del sistema -->
		        <div class="col-md-4">
		        	<div class="jumbotron" style="text-align:center;">
		        		<img src="<?= base_url('img/logo-unsa2.png'); ?>">
		        	</div>
		        </div>
		        <!-- Contenido de la aplicación -->
		        <div class="col-md-8">
		        	<?= $this->load->view($contenido); ?>
		        </div>
      		</div>
		    <hr>

		    <footer>
		    	<p><?= $this->session->userdata('nombre_usuario'); ?>&copy; Sistema de gestión de tickes UNSA 2014 - <?= date('d-m-Y H:i') ?> </p>
		    </footer>
		</div>
	</div>
</body>
</html>