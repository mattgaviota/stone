<div class="page-header">	
	<h1>Usuarios <small>mantenimiento de registros</small></h1>
</div>
<div class="row">
	<div class="filtros col-md-12">
		<fieldset>
		
		<div class="row filtro filtronombre">
			<div class="form-group">
				<label for="buscar_nombre" class="col-md-2">Por Nombre: </label>
				<div class="col-md-6">
					<div class="input-group">
						<input id="buscar_nombre" name="buscar_nombre" type="text" class="form-control" value=""/>
						<span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
					</div>
				</div>
			</div>
		</div>
		
		<br>

		<div class="row filtro filtrodni">
			<div class="form-group">
				<label for="buscar_dni" class="col-md-2">Por dni: </label>
				<div class="col-md-6">
					<div class="input-group">						
						<input id="buscar_dni" name="buscar_dni" type="text" class="form-control" />
						<span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
					</div>
				</div>	
			</div>
		</div>

		<br>

		<div class="row filtro filtrolu">
			<div class="form-group">
				<label for="buscar_lu" class="col-md-2">Por L.U: </label>
				<div class="col-md-6">
					<div class="input-group">						
						<input id="buscar_lu" name="buscar_lu" type="text" class="form-control" />
						<span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
					</div>
				</div>
				<div class="col-md-3">
					<div class="input-group">
				   		<?= anchor('usuarios/create', ' Agregar', array('class' => 'btn btn-primary glyphicon glyphicon-plus'));?>
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
				<th> DNI </th>
				<th> Nombre </th>
				<th> L.u </th>
				<th> Facultad </th>
				<th> Categoría </th>
				<th> Edición </th>
			</tr>
		</thead>

		<tbody id="destino_resultado">
			<?php foreach ($registros as $registro): ?>
			<tr class="<?php if($registro->estado == 0){echo 'danger';}else if($registro->estado == 3){echo 'warning';} ?>">
				<td><?= $registro->dni; ?></td>
				<td><?= $registro->nombre; ?></td>
				<td><?= $registro->lu; ?></td>
				<td><?= $registro->facultad_nombre; ?></td>
				<td><?= $registro->categoria_nombre; ?></td>
				<td><?= anchor('usuarios/edit/'.$registro->dni, ' ', array('class' => 'glyphicon glyphicon-pencil')); ?></td>
			</tr>
			<?php endforeach; ?>
		</tbody>
	</table>
</div>

<script type="text/javascript">
	base_url = '<?=base_url(); ?>';
</script>
<script src="<?= base_url('js/usuarios.js')?>"></script>