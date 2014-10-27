<?= form_open('index.php/usuarios/update', array('class'=>'form-horizontal jumbotron')); ?>
	<legend>Editando un Registro</legend>

	<?= my_validation_errors(validation_errors()); ?>

	<div class="row">
		<div class="form-group">
			<?= form_label('DNI: ', 'dni', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-4">
				<input class="form-control" type="text" name="dni" value="<?= $registro->dni; ?>" disabled/>
				<?= form_hidden('dni', $registro->dni); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Nombre: ', 'nombre', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-4">
				<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'nombre', 'id'=>'nombre','value'=>$registro->nombre)); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Email: ', 'email', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-4">
				<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'email', 'id'=>'email','value'=>$registro->email)); ?>
			</div>
		</div>
	</div>	

	<div class="row">
		<div class="form-group">
			<?= form_label('Libreta Universitaria: ', 'lu', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-4">
				<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'lu', 'id'=>'lu','value'=>$registro->lu)); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Facultad: ', 'id_facultad', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-4">
				<?= form_dropdown('id_facultad', $facultades, $registro->id_facultad, "class='form-control'"); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Provincia: ', 'id_provincia', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-4">
				<?= form_dropdown('id_provincia', $provincias, $registro->id_provincia, "class='form-control'"); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Perfil: ', 'id_perfil', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-4">
				<?= form_dropdown('id_perfil', $perfiles, $registro->id_perfil,"class='form-control'"); ?>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="form-group">
			<?= form_label('Categoría: ', 'id_categoria', array('class'=>'col-md-3 control-label')); ?>
			<div class="col-md-4">
				<?= form_dropdown('id_categoria', $categorias, $registro->id_categoria,"class='form-control'"); ?>
			</div>
		</div>
	</div>	

	<hr>

	<div class="form-group">
		<div class="col-sm-offset-2">
			<?= form_button(array('type'=>'submit', 'content'=>'Aceptar', 'class'=>'btn btn-success glyphicon glyphicon-ok')); ?>
			<?= anchor('usuarios/index', 'Cancelar',array('class'=>'btn btn-default glyphicon glyphicon-remove')); ?>
			<?= anchor('usuarios/delete/'.$registro->dni, 'Eliminar',array('class'=>'btn btn-danger glyphicon glyphicon-trash', 'onClick'=>"return confirm('¿Estas Seguro?');")); ?>
		</div>
	</div>

<?= form_close(); ?>