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

	<h3>Informe de cantidad  de tickets vendidos por Facultad y categoría de comensal</h3>
	<h4><?= ($desde === $hasta)? "En el día $desde":"Desde: $desde hasta: $hasta" ?></h4>
	<br />
	<br />

	<table class="table table-bordered table-striped table-hover">
		<thead>
			<tr>
				<th> Facultades </th>
				<th> Tickets Consumidos </th>
				<th> Regulares </th>
				<th> Becados </th>
				<th> Gratuitos </th>
				<th> Total en $ </th>
			</tr>
		</thead>
		<tbody id="resultado_tickets_tabla">
			<?php foreach ($registros2 as $registro2): ?>
			<tr>
				<td><?= $registro2->facultad; ?></td>
				<td><?= $registro2->total_tickets; ?></td>
				<td><?= $registro2->becados; ?></td>
				<td><?= $registro2->regulares; ?></td>
				<td><?= $registro2->gratuitos; ?></td>
				<td><?= $registro2->total_pesos; ?></td>
			</tr>
			<?php endforeach; ?>
			<tr class="info">
				<td>Totales: </td>
				<td><?= $totales2->total_tickets; ?></td>
				<td><?= $totales2->becados; ?></td>
				<td><?= $totales2->regulares; ?></td>
				<td><?= $totales2->gratuitos; ?></td>
				<td><?= $totales2->total_importe; ?></td>
			</tr>
		</tbody>
	</table>
</body>
</html>