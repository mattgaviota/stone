<div class="col-md-6">
	<div id="info-perfil" class="jumbotron">
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
			</div>
			</fieldset>
		</div>
		<br>
		<div class="row">
			<table class="table table-condensed table-bordered table-striped table-hover">
				<thead>
					<tr>
						<th> Fecha </th>
						<th> Acción </th>
						<th> Lugar </th>
					</tr>
				</thead>

				<tbody>
					<?php foreach ($acciones as $accion): ?>
					<tr>
						<td><?= $accion->fecha; ?></td>
						<td><?= $accion->nombre_accion; ?></td>
						<td><?= $accion->lugar; ?></td>
					</tr>
					<?php endforeach; ?>
				</tbody>
			</table>

		</div>
	</div>
</div>

<div class="col-md-6">
	<div id="operaciones-menu" class="jumbotron">
			
	</div>
</div>