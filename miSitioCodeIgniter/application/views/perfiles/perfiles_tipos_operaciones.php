<div class="row jumbotron">
	<h2 class="titulos">Permisos para las operaciones</h2>
	<div class="col-md-6">
		<table class="table table-condensed table-bordered table-striped table-hover">
			<caption><h3>Asignados</h3></caption>
			<thead>
			<tr>
				<th>ID</th>
				<th>Nombre</th>
				<th></th>
			</tr>
			</thead>
			<tbody>
			<?php foreach ($query_izq as $reg): ?>
			<tr>
				<td><?= $reg[0]; ?></td>
				<td><?= $reg[1]; ?></td>
				<td><?= anchor('perfiles/pto_noasignados/'.$reg[0].'/'.$reg[2],'<i class="glyphicon glyphicon-arrow-right"></i>'); ?></td>
			</tr>
			<?php endforeach; ?>      					
			</tbody>
		</table>
	</div>
	<div class="col-md-6">
		<table class="table table-condensed table-bordered table-striped table-hover">
			<caption><h3>No Asignados</h3></caption>
			<thead>
			<tr>
				<th></th>
				<th>ID</th>
				<th>Nombre</th>
			</tr>
			</thead>
			<tbody>
			<?php foreach ($query_der as $reg): ?>
			<tr>
				<td><?= anchor('perfiles/pto_asignados/'.$reg[0].'/'.$reg[2],'<i class="glyphicon glyphicon-arrow-left"></i>'); ?></td>
				<td><?= $reg[0]; ?></td>
				<td><?= $reg[1]; ?></td>
			</tr>
			<?php endforeach; ?>
			</tbody>
		</table>
	</div>
</div>
<div class="row">
	<div class="col-md-offset-10">
        <?= anchor('perfiles/index', ' Volver', 'class="btn btn-primary glyphicon glyphicon-arrow-left"'); ?>
	</div>
</div>

