<div class="row">
	<h3>Informes Estadísticos</h3>
	<div role="tabpanel">
		<!-- Nav tabs -->
		<ul class="nav nav-tabs" role="tablist">
		<li role="presentation" class="active"><a href="#informe1" aria-controls="informe1" role="tab" data-toggle="tab">Clasificación de Usuarios</a></li>
		<li role="presentation"><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">Servicios por Facultad</a></li>
		</ul>

		<!-- Tab panes -->
		<div class="tab-content">
			<div role="tabpanel" class="tab-pane active" id="informe1">
				<br>
				<table class="table table-bordered table-striped table-hover">
					<thead>
						<tr>
							<th> Facultades </th>
							<th> Total de Usuarios </th>
							<th> Becados </th>
							<th> Regulares </th>
							<th> Gratuitos </th>
						</tr>
					</thead>

					<tbody>
						<?php foreach ($registros as $registro): ?>
						<tr>
							<td><?= $registro->facultad; ?></td>
							<td><?= $registro->total_usuarios; ?></td>
							<td><?= $registro->becados; ?></td>
							<td><?= $registro->regulares; ?></td>
							<td><?= $registro->gratuitos; ?></td>
						</tr>
						<?php endforeach; ?>
						<tr class="info">
							<td>Totales: </td>
							<td><?= $totales->total_usuarios; ?></td>
							<td><?= $totales->becados; ?></td>
							<td><?= $totales->regulares; ?></td>
							<td><?= $totales->gratuitos; ?></td>
						</tr>
					</tbody>
				</table>
				<div class="col-md-offset-9">
					<?= form_open('index.php/reportes/generar_pdf'); ?>
						<input type="submit" class="btn btn-primary glyphicon glyphicon-print" value=" Descargar PDF" name="PDF1">
					<?= form_close(); ?>
				</div>
			</div>
			<div role="tabpanel" class="tab-pane" id="profile">
				<br>
				<table class="table table-condensed table-bordered table-striped table-hover">
					<thead>
						<tr>
							<th> Facultades </th>
							<th> asdas </th>
							<th> Creado </th>
							<th> Modificado </th>
							<th> Edición </th>
							<th> Permisos </th>
						</tr>
					</thead>

					<tbody>
							
					</tbody>
				</table>				

			</div>

		</div>
	</div>	
</div>
