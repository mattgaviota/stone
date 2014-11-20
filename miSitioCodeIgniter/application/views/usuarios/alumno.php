<div class="col-md-6">
	<div id="info-perfil" class="jumbotron">
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
					<label>Facultad: </label>
					<label class="mostrar-info"><?= $registro->facultad_nombre; ?></label>
				</div>

				<div class="form-group">
					<label>Provincia: </label>
					<label class="mostrar-info"><?= $registro->provincia_nombre; ?></label>
				</div>

				<div class="form-group">
					<label>Categoría: </label>
					<label class="mostrar-info"><?= $registro->categoria_nombre; ?></label>
				</div>

				<div class="form-group">
					<label>Saldo: </label>
					<label class="mostrar-info"><?= '$ '.$registro->saldo; ?></label>
				</div>
			</div>
			</fieldset>
		</div>
	</div>
</div>

<div class="col-md-6">
	<div id="botonera" class="jumbotron">
		<legend>Acciones Disponibles</legend>
		<div class="par-botones">
			<input type="button" value="Comprar" style="background-image: url('../img/ticket.png')" onclick="location.href='<?php echo base_url();?>usuarios/comprar_tickets'">
			<input type="button" value="Anular" style="background-image: url('../img/anular.png')" onclick="location.href='<?php echo base_url();?>usuarios/anular'">
		</div>
		<div class="par-botones">
			<input type="button" value="Imprimir" style="background-image: url('../img/printer.png')" onclick="location.href='<?php echo base_url();?>usuarios/imprimir'">
			<input type="button" value="Editar Perfil" style="background-image: url('../img/editar.png')" onclick="location.href='<?php echo base_url();?>usuarios/editar_perfil'">
		</div>
	</div>
</div>