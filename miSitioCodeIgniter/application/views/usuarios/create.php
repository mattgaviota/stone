<?= form_open('index.php/usuarios/insert', array('class'=>'form-horizontal jumbotron')); ?>
	<legend>Agregando un Registro</legend>

	<?= my_validation_errors(validation_errors()); ?>

	<div class="form-group">
		<?= form_label('Nombre: ', 'nombre', array('class'=>'col-sm-2 control-label')); ?>
		<?= form_input(array('type'=>'text', 'name'=>'nombre', 'id'=>'nombre','value'=>set_value('nombre'))); ?>
	</div>

	<div class="form-group">
		<?= form_label('Login: ', 'login', array('class'=>'col-sm-2 control-label')); ?>
		<?= form_input(array('type'=>'text', 'name'=>'login', 'id'=>'login','value'=>set_value('login'))); ?>
	</div>

	<div class="form-group">
		<?= form_label('Email: ', 'email', array('class'=>'col-sm-2 control-label')); ?>
		<?= form_input(array('type'=>'email', 'name'=>'email', 'id'=>'email','value'=>set_value('email'))); ?>
	</div>

	<div class="form-group">
		<?= form_label('Perfil: ', 'perfil_id', array('class'=>'col-sm-2 control-label')); ?>
		<?= form_dropdown('perfil_id', $perfiles, 0); ?>
	</div>

	<hr>

	<div class="form-group">
		<div class="col-sm-offset-2">
			<?= form_button(array('type'=>'submit', 'content'=>'Aceptar', 'class'=>'btn btn-success')); ?>
			<?= anchor('usuarios/index', 'Cancelar',array('class'=>'btn btn-warning')); ?>
		</div>
	</div>
<?= form_close(); ?>