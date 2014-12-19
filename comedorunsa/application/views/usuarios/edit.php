<?= form_open('index.php/usuarios/update', array('class'=>'form-horizontal jumbotron')); ?>
	<legend>Editando un Registro</legend>

	<?= my_validation_errors(validation_errors()); ?>

	<div class="row">
		<div class="form-group">
			<?= form_label('Usuario: ', 'dni', array('class'=>'col-md-3 control-label')); ?>
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

	<div class="row">
		<div class="form-group">
      		<label class="col-md-3 control-label">Estado: </label>
      		<div class="col-md-4">
        		<div class="radio">
          			<label>
            		<input name="estado" id="activo" value="2" <?php if($registro->estado == 2){ echo 'checked';}?> type="radio">
            		Activo
          			</label>
        		</div>
        		<div class="radio">
          			<label>
           	 		<input name="estado" id="bloqueado" value="0" <?php if($registro->estado == 0){ echo 'checked';}?> type="radio">
            		Bloqueado
          			</label>
        		</div>
      		</div>
		</div>
	</div>

	<hr>

	<div class="form-group">
		<div class="col-sm-offset-2">
			<?= form_button(array('type'=>'submit', 'content'=>' Aceptar', 'class'=>'btn btn-success glyphicon glyphicon-ok')); ?>
			<?= anchor('usuarios/index', ' Cancelar',array('class'=>'btn btn-default glyphicon glyphicon-remove')); ?>
		</div>
	</div>
<?= form_close(); ?>