<h2>Tu Perfil <small>modifiquelo a gusto</small></h2>
<hr>
<div class="col-md-4">
	<div id="datos-no-editables" class="jumbotron">
		<div class="row">
			<legend>Datos No Editables</legend>
			<fieldset>
				<div class="col-xs-12">
			    	<a href="#" class="thumbnail">
						<?= form_open_multipart('index.php/usuarios/subir_foto', array('id'=>'form-foto')); ?>
			      			<input type="file" name="userfile" style="visibility:hidden;position:absolute;top:0;"/>
			      		<?= form_close(); ?>
			      		<img class="img-subir" data-src="holder.js/100%x180" style="width: 100%;height:200px;" src="<?= $registro->ruta_foto; ?>">
			    	</a>

					<hr>

					<div class="form-group">
						<label>DNI: </label>
						<label class="mostrar-info"><?= $registro->dni; ?></label>
					</div>

					<div class="form-group">
						<label>L.U: </label>
						<label class="mostrar-info"><?= $registro->lu; ?></label>
					</div>

					<div class="form-group">
						<label>Categoría: </label>
						<label class="mostrar-info"><?= $registro->categoria_nombre; ?></label>
					</div>

					<div class="form-group">
						<label>Saldo: </label>
						<label class="mostrar-info"><?= '$ '.$registro->saldo; ?></label>
					</div>
				</div>
			</fieldset>
		</div>
	</div>
</div>
<div class="col-md-8">
	<div id="datos-editables" class="jumbotron">
	<legend>Datos Editables</legend>
	
	<?= form_open_multipart('index.php/usuarios/editando_perfil', array('class'=>'form-horizontal')); ?>
	<fieldset>
	<div>
		<?= my_validation_errors(validation_errors()); ?>
		<div class="row">
			<div class="form-group">
					<?= form_hidden('dni', $registro->dni); ?>
			</div>
		</div>

		<div class="row">
			<div class="form-group">
				<?= form_label('Nombre: ', 'nombre', array('class'=>'col-md-3 control-label')); ?>
				<div class="col-md-8">
					<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'nombre', 'id'=>'nombre','value'=>$registro->nombre)); ?>
				</div>
			</div>
		</div>

		<div class="row">
			<div class="form-group">
				<?= form_label('Email: ', 'email', array('class'=>'col-md-3 control-label')); ?>
				<div class="col-md-8">
					<?= form_input(array('class'=>'form-control','type'=>'text', 'name'=>'email', 'id'=>'email','value'=>$registro->email)); ?>
				</div>
			</div>
		</div>	

		<div class="row">
			<div class="form-group">
				<?= form_label('Facultad: ', 'id_facultad', array('class'=>'col-md-3 control-label')); ?>
				<div class="col-md-8">
					<?= form_dropdown('id_facultad', $facultades, $registro->id_facultad, "class='form-control'"); ?>
				</div>
			</div>
		</div>

		<div class="row">
			<div class="form-group">
				<?= form_label('Provincia: ', 'id_provincia', array('class'=>'col-md-3 control-label')); ?>
				<div class="col-md-8">
					<?= form_dropdown('id_provincia', $provincias, $registro->id_provincia, "class='form-control'"); ?>
				</div>
			</div>
		</div>

		<hr>

		<div class="form-group">
			<div class="col-sm-offset-7">
				<?= form_button(array('type'=>'submit', 'content'=>'Aceptar', 'class'=>'btn btn-success glyphicon glyphicon-ok')); ?>
				<?= anchor('usuarios/alumno', ' Volver',array('class'=>'btn btn-primary glyphicon glyphicon-arrow-left')); ?>
			</div>
		</div>
	</div>
	</fieldset>	
	<?= form_close(); ?>
	
	</div>
</div>

<script src="<?= base_url('js/cambiar-foto.js'); ?>"></script>