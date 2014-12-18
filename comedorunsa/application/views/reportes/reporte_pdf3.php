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

	<h3>Informe con el estado de los tickets por Facultad </h3>
	<h4><?= ($desde === $hasta)? "En el día $desde":"Desde: $desde hasta: $hasta" ?></h4>
	<br />
	<br />

	<table class="table table-bordered table-striped table-hover">
		<thead>
			<tr>
				<th> Facultades </th>
				<th> Total de Tickets </th>
				<th> Anulados </th>
				<th> Activos </th>
				<th> Impresos </th>
				<th> Consumidos </th>
			</tr>
		</thead>
		<tbody id="resultado_tickets_tabla2">
			<?php foreach ($registros3 as $registro3): ?>
			<tr>
				<td><?= $registro3->facultad; ?></td>
				<td><?= $registro3->total_tickets; ?></td>
				<td><?= $registro3->anulados; ?></td>
				<td><?= $registro3->activos; ?></td>
				<td><?= $registro3->impresos; ?></td>
				<td><?= $registro3->consumidos; ?></td>
			</tr>
			<?php endforeach; ?>
			<tr class="info">
				<td>Totales: </td>
				<td><?= $totales3->total_tickets; ?></td>
				<td><?= $totales3->anulados; ?></td>
				<td><?= $totales3->activos; ?></td>
				<td><?= $totales3->impresos; ?></td>
				<td><?= $totales3->consumidos; ?></td>
			</tr>
		</tbody>
	</table>
</body>
</html>