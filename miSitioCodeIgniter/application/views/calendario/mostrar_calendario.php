<div class="jumbotron">
	<div class="row">
		<div class="col-md-8">
			<h2>Calendario académico</h2>
		</div>
	</div>
	<div class="row">
		<div class="col-md-7">
			<?= $calendario; ?>
			<script src="<?= base_url('js/calendario-ajax.js'); ?>"></script>
		</div>
		<div class="col-md-5">
			<div class="panel panel-info">
				<div class="panel-heading">
					<h3 class="panel-title">Panel info</h3>
				</div>
				<div class="panel-body">
					<form id="resultadoCalendario" action="http://localhost/miSitioCodeIgniter/index.php/calendario/actualizar" method="post">
					</form>
					<br>
					<span id="mensaje"></span>
				</div>
			</div>
		</div>
	</div>
</div>





