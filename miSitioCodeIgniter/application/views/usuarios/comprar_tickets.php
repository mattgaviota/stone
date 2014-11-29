<h2>Compre sus tickets <small>haciendo clicks</small></h2>
<hr>
<div class="col-md-6">
	<div id="info-relevante" class="jumbotron">
		<div class="row">
			<legend>Información personal</legend>
			<fieldset>
			<div class="col-xs-5">
				<a href="#" class="thumbnail">
					<img data-src="holder.js/100%x180" style="width: 100%;" src="<?= $registro->ruta_foto; ?>">
				</a>
			</div>
			<div class="col-xs-7">
				<div class="form-group">
					<label>Nombre: </label>
					<label class="mostrar-info"><?= $registro->nombre; ?></label>
				</div>
				<div class="form-group">
					<label>DNI: </label>
					<label class="mostrar-info"><?= $registro->dni; ?></label>
				</div>
				<div class="form-group">
					<label>Categoría: </label>
					<label class="mostrar-info"><?= $registro->categoria_nombre; ?></label>
				</div>
				<div class="form-group">
					<label>Saldo en $: </label>
					<label class="mostrar-info"><?= $registro->saldo; ?></label>
				</div>
			</div>
			</fieldset>
		</div>
	</div>

	<div id="referencias" class="jumbotron">
		<div class="row">
			<legend>Referencias</legend>
			<table class="table table-condensed table-bordered table-striped table-hover">
				<thead>
					<tr>
						<th>Color</th>
						<th>Descripción</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<th style="background-color: #2ecc71"></th>
						<th>Día confirmado</th>
					</tr>
					<tr>
						<th style="background-color: #f1c40f"></th>
						<th>Día seleccionado para la compra, pero falta confirmación</th>
					</tr>
					<tr>
						<th style="background-color: #FFB9C4"></th>
						<th>Día no hábil para realizar una compra</th>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</div>
<div class="col-md-6">
	<div id="calendario" class="jumbotron">
		<div class="row">
			<script type="text/javascript">
				base_url = '<?=base_url(); ?>';
			</script>
			<script src="<?= base_url('js/calendario-comprar.js'); ?>"></script>
			<?= $calendario; ?>
		</div>

		<br>
		
		<div class="row">
			<button id="enviar-info" class="btn btn-success glyphicon glyphicon-ok"> Confirmar</button>
			<?= anchor('usuarios/alumno', ' Volver',array('class'=>'btn btn-primary glyphicon glyphicon-arrow-left')); ?>
			<br>
			<div id="respuesta-compra"></div>
		</div>
	</div>
</div>

