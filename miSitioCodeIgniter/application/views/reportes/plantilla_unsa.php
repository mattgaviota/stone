<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="./css/estilos-pdf.css">
</head>
<body>
	<header>
		<div id="img-unsa-logo">
			<img src="./img/logomejorado.png">
			
		</div>
		<div id="info-encabezado">	
			<h3>Universidad Nacional de Salta</h3>
			<h3>Comedor Universitario</h3>
			<h5>Avda. Bolivia 5150-Salta-4400</h5>
			<h5>Tel. 54-0387-425521</h5>
			<h5>Correo Electrónico: seccosu@unsa.edu.ar</h5>
		</div>
		<hr>
	</header>

	<h3>Informe de cantidad  de usuarios por Facultad y categoría de comensal</h3>
	<br />
	<br />

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
</body>
</html>