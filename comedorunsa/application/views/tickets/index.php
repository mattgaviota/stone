<div class="page-header">
	<h1>Tickets <small>Consulta de Registros</small></h1>
</div>

<div class="row">
	<div class="filtros col-md-12">
		<fieldset>
		<div class="col-md-6">
			<div class="row filtro filtronombre">
				<div class="form-group">
					<label for="buscar_nombre" class="col-md-2">Nombre: </label>
					<div class="col-md-10">
						<div class="input-group">
							<input id="buscar_nombre" name="buscar_nombre" type="text" class="form-control" value="" placeholder="Filtrar por Nombre" />
							<span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
						</div>
					</div>
				</div>
			</div>
			<br>
			<div class="row filtro filtrodni">
				<div class="form-group">
					<label for="buscar_dni" class="col-md-2">Dni: </label>
					<div class="col-md-10">
						<div class="input-group">						
							<input id="buscar_dni" name="buscar_dni" type="text" class="form-control" placeholder="Filtrar por dni" />
							<span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
						</div>
					</div>	
				</div>
			</div>
		</div>
		
		<div class="col-md-6">
			<div class="row filtro filtrolu">
				<div class="form-group">
					<label for="buscar_id" class="col-md-2">ID: </label>
					<div class="col-md-10">
						<div class="input-group">						
							<input id="buscar_id" name="buscar_id" type="text" class="form-control" placeholder="Filtrar por ID de ticket" />
							<span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
						</div>
					</div>
				</div>
			</div>
			<br>
			<div class="row filtro filtrolu">
				<div class="form-group">
					<label for="buscar_fecha" class="col-md-2">Fecha: </label>
					<div class="col-md-10">
						<div class="input-group">						
							<input id="buscar_fecha" name="buscar_fecha" type="text" class="form-control" placeholder="Filtrar por fecha" />
							<span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
						</div>
					</div>
				</div>
			</div>
		</div>

		</fieldset>
	</div>
</div>

<br>

<div class="tablas-propias">
	<table class="table table-bordered table-striped table-hover">
		<thead>
			<tr>
				<th> ID </th>
				<th> Fecha </th>
				<th> Importe </th>
				<th> Estado </th>
				<th> DNI </th>
				<th> Nombre </th>
				<th> Detalle </th>
			</tr>
		</thead>

		<tbody id="destino_resultado">
			<?php foreach ($registros as $registro): ?>
			<tr>
				<td><?= $registro->id_ticket; ?></td>
				<td><?= date("d/m/Y",strtotime($registro->fecha)); ?></td>
				<td><?= $registro->importe_ticket; ?></td>
				<td><?= $registro->estado_ticket; ?></td>
				<td><?= $registro->dni; ?></td>
				<td><?= $registro->nombre_usuario; ?></td>
				<td><?= anchor('tickets/detalles/'.$registro->id_ticket, ' ', array('class' => 'glyphicon glyphicon-search')); ?></td>
			</tr>
			<?php endforeach; ?>
		</tbody>
	</table>
</div>

<script type="text/javascript">
	base_url = '<?=base_url(); ?>';
</script>
<script src="<?= base_url('js/tickets.js')?>"></script>
