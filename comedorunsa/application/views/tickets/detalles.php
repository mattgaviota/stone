<div class="page-header">
	<h1>El camino del ticket</h1>
</div>

<div class="col-md-offset-10">
	<?= anchor('tickets/index', ' Volver', array('class' => 'btn btn-primary glyphicon glyphicon-arrow-left')); ?>
</div>

<br>

<div class="tablas-propias">
	<table class="table table-bordered table-striped table-hover">
		<thead>
			<tr>
				<th> ID_ticket </th>
				<th> ID_log </th>
				<th> Fecha </th>
				<th> Acción </th>
				<th> Lugar </th>
			</tr>
		</thead>

		<tbody>
			<?php foreach ($registros as $registro): ?>
			<tr>
				<td><?= $registro->id_ticket; ?></td>
				<td><?= $registro->id_log; ?></td>
				<td><?= date("d/m/Y H:i:s",strtotime($registro->fecha)); ?></td>
				<td><?= $registro->accion; ?></td>
				<td><?= ($registro->lugar == 1)? 'Web':'Máquina'; ?></td>
			</tr>
			<?php endforeach; ?>
		</tbody>
	</table>
</div>
