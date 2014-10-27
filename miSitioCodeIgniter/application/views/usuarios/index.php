<div class="page-header">	
	<h1>Usuarios <small>mantenimiento de registros</small></h1>
</div>

<?= form_open('index.php/usuarios/search', array('class' => 'form-search')); ?>
	<div class="row" style="margin:1em 0;">
		<div class="col-md-4">
			<div class="input-group">
	        <input type="text" class="form-control" placeholder="Buscar por nombre" name="buscar" id="buscar">
	        <div class="input-group-btn">
	            <button class="btn btn-default" type="submit"><i class="glyphicon glyphicon-search"></i></button>  
	        </div>
	    </div>
		</div>
		<div class="col-md-4">
			<div class="input-group">
	       		<?= anchor('usuarios/create', ' Agregar', array('class' => 'btn btn-primary glyphicon glyphicon-plus'));?>
	    	</div>
		</div>
	</div>
<?= form_close(); ?>

<table class="table table-condensed table-bordered table-striped table-hover">
	<thead>
		<tr>
			<th> DNI </th>
			<th> Nombre </th>
			<th> Email </th>
			<th> L.u </th>
			<th> Facultad </th>
			<th> Provincia </th>
			<th> Perfil </th>
			<th> Categoría </th>
			<th> Edición </th>
		</tr>
	</thead>

	<tbody>
		<?php foreach ($registros as $registro): ?>
		<tr>
			<td><?= $registro->dni; ?></td>
			<td><?= $registro->nombre; ?></td>
			<td><?= $registro->email; ?></td>
			<td><?= $registro->lu; ?></td>
			<td><?= $registro->facultad_nombre; ?></td>
			<td><?= $registro->provincia_nombre; ?></td>
			<td><?= $registro->perfil_nombre; ?></td>
			<td><?= $registro->categoria_nombre; ?></td>
			<td><?= anchor('usuarios/edit/'.$registro->dni, ' Editar', array('class' => 'btn btn-info glyphicon glyphicon-pencil')); ?></td>
		</tr>
		<?php endforeach; ?>
	</tbody>
</table>