<h2>Compre sus tickets <small>haciendo clicks</small></h2>
<hr>
<div class="col-md-6">
	<div id="info-relevante" class="jumbotron">
		<div class="row">
			<fieldset>
			<legend>Información personal</legend>
			<div class="col-xs-5">
				<img style="width: 100%;" src="<?= base_url('img/user.jpg'); ?>">
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
</div>
<div class="col-md-6">
	<div id="calendario" class="jumbotron">
		<script src="<?= base_url('js/calendario-comprar.js'); ?>"></script>
		<?= $calendario; ?>
		<br>

		<input class="input-control btn btn-primary" value="confirmar">
	</div>
</div>