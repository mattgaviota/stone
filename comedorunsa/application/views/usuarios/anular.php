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
	<div id="tickets-anulables" class="jumbotron">
		<legend>Anular Tickets</legend>
		<table class="table table-condensed table-bordered table-striped table-hover">
			<thead>
				<tr>
					<th> Número </th>
					<th> Fecha </th>
					<th> Importe </th>
					<th> Estado </th>
					<th> Anular </th>
				</tr>
			</thead>

			<tbody>
				<?php foreach ($tickets_proximos as $ticket): ?>
				<tr>
					<td><?= $ticket->id; ?></td>
					<td><?= $ticket->fecha_ticket; ?></td>
					<td><?= $ticket->importe; ?></td>
					<td><?= ($ticket->estado == 1)?"Activo":"Anulado"; ?></td>
					<td><?= anchor('usuarios/anulando_ticket/'.$ticket->id, ' Anular',array('class'=>'btn btn-danger glyphicon glyphicon-trash', 'onClick'=>"return confirm('¿Estas Seguro?');")); ?></td>
				</tr>
				<?php endforeach; ?>
			</tbody>
		</table>
		<div class="row">
			<div class="col-md-offset-9">
				<?= anchor('usuarios/alumno', ' Volver',array('class'=>'btn btn-primary glyphicon glyphicon-arrow-left')); ?>
			</div>
		</div>
	</div>
</div>